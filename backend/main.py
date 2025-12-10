# main.py
# CreditPilot - FastAPI后端主文件

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timedelta
import os
import shutil
from pathlib import Path

from models import (
    Statement, Transaction, Document, Client, ReminderLog,
    get_db, SessionLocal
)
from datetime import date
from pdf_parser import parse_alliance_bank_statement
from classification_engine import (
    classify_all_transactions,
    calculate_miscellaneous_fee,
    calculate_balances
)
from reminder_system import generate_daily_reminder, generate_excel_report
from csv_importer import import_csv_file

# FastAPI应用初始化
app = FastAPI(
    title="CreditPilot API",
    description="信用卡账单管理系统API",
    version="1.0.0"
)

# CORS配置（允许iPad App访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/app/uploads"))
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "/app/reports"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ====================================================
# 根路径
# ====================================================
@app.get("/")
async def root():
    """API信息"""
    return {
        "name": "CreditPilot API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


# ====================================================
# Dashboard API
# ====================================================
@app.get("/api/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """获取Dashboard统计数据"""
    try:
        total_statements = db.query(Statement).filter(Statement.is_active == True).count()
        verified_statements = db.query(Statement).filter(
            Statement.is_active == True,
            Statement.is_verified == True
        ).count()
        
        # 计算总余额
        statements = db.query(Statement).filter(Statement.is_active == True).all()
        total_owner_balance = sum(s.owner_os_balance for s in statements)
        total_gz_balance = sum(s.gz_os_balance for s in statements)
        
        # 即将到期的账单（未来7天）
        today = date.today()
        upcoming_due_date = today + timedelta(days=7)
        upcoming_count = db.query(Statement).filter(
            Statement.is_active == True,
            Statement.due_date >= today,
            Statement.due_date <= upcoming_due_date
        ).count()
        
        return {
            "total_statements": total_statements,
            "verified_statements": verified_statements,
            "pending_verification": total_statements - verified_statements,
            "total_owner_balance": round(total_owner_balance, 2),
            "total_gz_balance": round(total_gz_balance, 2),
            "upcoming_due_count": upcoming_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/upcoming")
async def get_upcoming_statements(db: Session = Depends(get_db)):
    """获取未来2天到期的账单"""
    try:
        today = date.today()
        tomorrow = today + timedelta(days=1)
        day_after = today + timedelta(days=2)
        
        # 明天到期
        tomorrow_statements = db.query(Statement).filter(
            Statement.is_active == True,
            Statement.due_date == tomorrow
        ).all()
        
        # 后天到期
        day_after_statements = db.query(Statement).filter(
            Statement.is_active == True,
            Statement.due_date == day_after
        ).all()
        
        def format_statement(s: Statement):
            return {
                "id": s.id,
                "client_name": s.client_name,
                "card_number": s.card_number,
                "bank_name": s.bank_name,
                "due_date": str(s.due_date),
                "gz_payment": s.gz_payment_1,
                "owner_payment": s.owner_payment,
                "is_verified": s.is_verified,
                "document_count": len(s.documents)
            }
        
        return {
            "tomorrow": [format_statement(s) for s in tomorrow_statements],
            "day_after": [format_statement(s) for s in day_after_statements],
            "tomorrow_count": len(tomorrow_statements),
            "day_after_count": len(day_after_statements),
            "total_gz_payment": round(
                sum(s.gz_payment_1 for s in tomorrow_statements + day_after_statements), 2
            ),
            "total_owner_payment": round(
                sum(s.owner_payment for s in tomorrow_statements + day_after_statements), 2
            )
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ====================================================
# 账单管理 API
# ====================================================
@app.post("/api/statements/upload")
async def upload_statement(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传PDF账单并解析"""
    try:
        # 保存文件
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 解析PDF
        parsed_data = parse_alliance_bank_statement(str(file_path))
        
        # 分类交易
        classification_result = classify_all_transactions(parsed_data["transactions"])
        
        # 计算Miscellaneous Fee
        misc_fee = calculate_miscellaneous_fee(classification_result["gz_expenses"])
        
        # 计算余额
        balance_result = calculate_balances(
            previous_balance=parsed_data["previous_balance"],
            previous_balance_gz=parsed_data["previous_balance_gz"],
            owner_expenses=classification_result["owner_expenses"],
            gz_expenses=classification_result["gz_expenses"],
            miscellaneous_fee=misc_fee,
            owner_payment=0.0,  # 初始为0
            gz_payment_1=0.0  # 初始为0
        )
        
        # 创建Statement记录
        statement = Statement(
            client_name=parsed_data["client_name"],
            card_number=parsed_data["card_number"],
            bank_name=parsed_data["bank_name"],
            statement_date=parsed_data["statement_date"],
            due_date=parsed_data["due_date"],
            previous_balance=parsed_data["previous_balance"],
            previous_balance_gz=parsed_data["previous_balance_gz"],
            owner_expenses=classification_result["owner_expenses"],
            gz_expenses=classification_result["gz_expenses"],
            total_expenses=balance_result["total_expenses"],
            miscellaneous_fee=misc_fee,
            owner_os_balance=balance_result["owner_os_balance"],
            gz_os_balance=balance_result["gz_os_balance"],
            pdf_path=str(file_path),
            pdf_filename=file.filename,
            total_transactions=len(classification_result["transactions"]),
            verification_status="pending"
        )
        
        db.add(statement)
        db.flush()  # 获取ID
        
        # 创建Transaction记录
        for trans_data in classification_result["transactions"]:
            transaction = Transaction(
                statement_id=statement.id,
                transaction_date=trans_data["transaction_date"],
                description=trans_data["description"],
                amount=trans_data["amount"],
                supplier=trans_data["supplier"],
                is_gz_expense=trans_data["is_gz_expense"],
                is_owner_expense=trans_data["is_owner_expense"]
            )
            db.add(transaction)
        
        db.commit()
        db.refresh(statement)
        
        return {
            "success": True,
            "statement_id": statement.id,
            "message": "PDF解析成功",
            "data": {
                "client_name": statement.client_name,
                "card_number": statement.card_number,
                "statement_date": str(statement.statement_date),
                "due_date": str(statement.due_date),
                "total_transactions": statement.total_transactions,
                "owner_expenses": statement.owner_expenses,
                "gz_expenses": statement.gz_expenses,
                "miscellaneous_fee": statement.miscellaneous_fee,
                "verification_status": statement.verification_status
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


@app.get("/api/statements")
async def get_statements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取所有账单"""
    statements = db.query(Statement).filter(
        Statement.is_active == True
    ).offset(skip).limit(limit).all()
    
    return {
        "total": len(statements),
        "statements": [
            {
                "id": s.id,
                "client_name": s.client_name,
                "card_number": s.card_number,
                "bank_name": s.bank_name,
                "statement_date": str(s.statement_date),
                "due_date": str(s.due_date),
                "owner_os_balance": s.owner_os_balance,
                "gz_os_balance": s.gz_os_balance,
                "is_verified": s.is_verified,
                "verification_status": s.verification_status
            }
            for s in statements
        ]
    }


@app.get("/api/statements/{statement_id}")
async def get_statement(statement_id: int, db: Session = Depends(get_db)):
    """获取单个账单详情"""
    statement = db.query(Statement).filter(Statement.id == statement_id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="账单不存在")
    
    transactions = db.query(Transaction).filter(
        Transaction.statement_id == statement_id
    ).all()
    
    documents = db.query(Document).filter(
        Document.statement_id == statement_id
    ).all()
    
    return {
        "statement": {
            "id": statement.id,
            "client_name": statement.client_name,
            "card_number": statement.card_number,
            "bank_name": statement.bank_name,
            "statement_date": str(statement.statement_date),
            "due_date": str(statement.due_date),
            "previous_balance": statement.previous_balance,
            "previous_balance_gz": statement.previous_balance_gz,
            "owner_expenses": statement.owner_expenses,
            "gz_expenses": statement.gz_expenses,
            "total_expenses": statement.total_expenses,
            "miscellaneous_fee": statement.miscellaneous_fee,
            "owner_payment": statement.owner_payment,
            "gz_payment_1": statement.gz_payment_1,
            "gz_payment_2": statement.gz_payment_2,
            "owner_os_balance": statement.owner_os_balance,
            "gz_os_balance": statement.gz_os_balance,
            "is_verified": statement.is_verified,
            "verification_status": statement.verification_status,
            "total_transactions": statement.total_transactions
        },
        "transactions": [
            {
                "id": t.id,
                "transaction_date": str(t.transaction_date),
                "description": t.description,
                "amount": t.amount,
                "supplier": t.supplier,
                "is_gz_expense": t.is_gz_expense,
                "is_owner_expense": t.is_owner_expense
            }
            for t in transactions
        ],
        "documents": [
            {
                "id": d.id,
                "document_type": d.document_type,
                "file_name": d.file_name,
                "ocr_verified": d.ocr_verified
            }
            for d in documents
        ]
    }


# ====================================================
# 提醒系统 API
# ====================================================
@app.get("/api/reminders/test")
async def test_reminder(db: Session = Depends(get_db)):
    """立即测试提醒（不等到晚上10点）"""
    try:
        result = generate_daily_reminder(db)
        return {
            "success": True,
            "message": "提醒测试成功",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reminders/daily-report")
async def get_daily_report(db: Session = Depends(get_db)):
    """下载Excel日报"""
    try:
        report_path = generate_excel_report(db)
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="报告文件不存在")
        
        return FileResponse(
            report_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=os.path.basename(report_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ====================================================
# CSV导入 API
# ====================================================
@app.post("/api/import/csv")
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传并导入CSV文件"""
    try:
        # 保存文件
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 导入CSV
        result = import_csv_file(str(file_path))
        
        if result['success']:
            return {
                "success": True,
                "message": "CSV导入成功",
                "data": {
                    "imported": result['imported'],
                    "updated": result['updated'],
                    "skipped": result['skipped'],
                    "total": result['total']
                }
            }
        else:
            raise HTTPException(status_code=400, detail=result.get('error', '导入失败'))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")


# ====================================================
# 单据管理 API
# ====================================================
@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    statement_id: Optional[int] = Form(None),
    document_type: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    上传单据（Merchant Receipt / Payment Slip / Transfer Slip）
    
    参数：
    - file: 文件（图片或PDF）
    - statement_id: 账单ID（可选，如果不提供需要手动关联）
    - document_type: 单据类型（Merchant Slip / Payment Receipt / Transfer Slip）
    """
    try:
        # 验证单据类型
        valid_types = ["Merchant Slip", "Payment Receipt", "Transfer Slip", "Statement"]
        if document_type and document_type not in valid_types:
            raise HTTPException(
                status_code=400, 
                detail=f"单据类型无效。有效类型：{', '.join(valid_types)}"
            )
        
        # 验证账单是否存在
        statement = None
        if statement_id:
            statement = db.query(Statement).filter(Statement.id == statement_id).first()
            if not statement:
                raise HTTPException(status_code=404, detail="账单不存在")
        
        # 保存文件
        file_ext = Path(file.filename).suffix.lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.gif']
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式。支持格式：{', '.join(allowed_extensions)}"
            )
        
        # 创建文件保存路径
        documents_dir = UPLOAD_DIR / "documents"
        documents_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = documents_dir / safe_filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 创建Document记录
        document = Document(
            statement_id=statement_id if statement else None,
            document_type=document_type or "Statement",
            file_path=str(file_path),
            file_name=file.filename,
            upload_date=date.today(),
            ocr_verified=False
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        return {
            "success": True,
            "message": "单据上传成功",
            "data": {
                "document_id": document.id,
                "document_type": document.document_type,
                "file_name": document.file_name,
                "statement_id": document.statement_id,
                "upload_date": str(document.upload_date)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


@app.get("/api/documents")
async def get_documents(
    statement_id: int = None,
    document_type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取单据列表"""
    query = db.query(Document)
    
    if statement_id:
        query = query.filter(Document.statement_id == statement_id)
    
    if document_type:
        query = query.filter(Document.document_type == document_type)
    
    documents = query.offset(skip).limit(limit).all()
    
    return {
        "total": len(documents),
        "documents": [
            {
                "id": d.id,
                "statement_id": d.statement_id,
                "document_type": d.document_type,
                "file_name": d.file_name,
                "upload_date": str(d.upload_date),
                "ocr_verified": d.ocr_verified,
                "matched_transaction_id": d.matched_transaction_id
            }
            for d in documents
        ]
    }


@app.get("/api/documents/{document_id}")
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """获取单个单据详情"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="单据不存在")
    
    return {
        "id": document.id,
        "statement_id": document.statement_id,
        "document_type": document.document_type,
        "file_name": document.file_name,
        "file_path": document.file_path,
        "upload_date": str(document.upload_date),
        "ocr_text": document.ocr_text,
        "ocr_verified": document.ocr_verified,
        "matched_transaction_id": document.matched_transaction_id,
        "matched_amount": document.matched_amount
    }


@app.get("/api/documents/{document_id}/download")
async def download_document(document_id: int, db: Session = Depends(get_db)):
    """下载单据文件"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="单据不存在")
    
    if not os.path.exists(document.file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 确定媒体类型
    file_ext = Path(document.file_path).suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.pdf': 'application/pdf',
        '.gif': 'image/gif'
    }
    media_type = media_types.get(file_ext, 'application/octet-stream')
    
    return FileResponse(
        document.file_path,
        media_type=media_type,
        filename=document.file_name
    )


@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """删除单据"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="单据不存在")
    
    try:
        # 删除文件
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # 删除数据库记录
        db.delete(document)
        db.commit()
        
        return {
            "success": True,
            "message": "单据已删除"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")


# ====================================================
# 启动服务器
# ====================================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
