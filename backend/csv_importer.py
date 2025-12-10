# csv_importer.py
# CreditPilot - CSV数据导入功能

import csv
import os
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from typing import List, Dict

from models import Statement, Transaction, Client, get_db, SessionLocal


def parse_csv_file(csv_path: str) -> List[Dict]:
    """
    解析CSV文件，提取账单信息
    
    Args:
        csv_path: CSV文件路径
        
    Returns:
        账单数据列表
    """
    statements = []
    current_statement = None
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # 跳过空行
            if not any(row.values()):
                continue
            
            # 尝试多种可能的列名格式（处理空格和大小写）
            # 注意：CSV列名后面可能有空格
            bank = (row.get('BANK ', '') or row.get('BANK', '') or 
                   row.get('bank ', '') or row.get('bank', '')).strip()
            client_name = (row.get('CLIENT NAME ', '') or row.get('CLIENT NAME', '') or 
                          row.get('client name ', '') or row.get('client name', '')).strip()
            card_no = (row.get('CARD NO ', '') or row.get('CARD NO', '') or 
                      row.get('card no ', '') or row.get('card no', '')).strip()
            statement_date_str = (row.get('Statement Date ', '') or row.get('Statement Date', '') or
                                 row.get('statement date ', '') or row.get('statement date', '')).strip()
            due_date_str = (row.get('Due Date ', '') or row.get('Due Date', '') or
                           row.get('due date ', '') or row.get('due date', '')).strip()
            
            # 如果这一行有银行和客户信息，说明是新账单
            if bank and client_name:
                # 保存上一个账单
                if current_statement:
                    statements.append(current_statement)
                
                # 创建新账单
                current_statement = {
                    'bank_name': bank,
                    'client_name': client_name,
                    'card_number': card_no.replace(' ', '')[-4:] if card_no else '',  # 取后4位
                    'full_card_number': card_no.replace(' ', ''),
                    'statement_date': parse_date(statement_date_str),
                    'due_date': parse_date(due_date_str),
                    'card_type': (row.get('Type ', '') or row.get('Type', '') or 
                                 row.get('type ', '') or row.get('type', '')).strip(),
                    'limit': (row.get('Limit ', '') or row.get('Limit', '') or 
                            row.get('limit ', '') or row.get('limit', '')).strip(),
                    'swipe_amount': parse_float(row.get('Swipe Amount ', '') or row.get('Swipe Amount', '')),
                    'due_amount': parse_float(row.get('Due Amount ', '') or row.get('Due Amount', '')),
                    'owner_expenses': parse_float(row.get("Owner's Expenses ", '') or row.get("Owner's Expenses", '')),
                    'gz_expenses': parse_float(row.get("GZ's Expenses ", '') or row.get("GZ's Expenses", '')),
                    'gz_payment': parse_float(row.get('GZ\'s Payment 1 + 2 ', '') or row.get('GZ\'s Payment 1 + 2', '')),
                    'gz_os_bal': parse_float(row.get("GZ's OS Bal ", '') or row.get("GZ's OS Bal", '')),
                    'owner_os_bal': parse_float(row.get("Owner's OS Bal ", '') or row.get("Owner's OS Bal", '')),
                    'remarks': (row.get('Remarks', '') or row.get('remarks', '')).strip(),
                    'points': (row.get('Points ', '') or row.get('Points', '') or 
                             row.get('points ', '') or row.get('points', '')).strip(),
                }
            # 如果只有卡号，说明是同一客户的另一张卡（share limit）
            elif card_no and current_statement:
                # 可以在这里处理多张卡的情况
                pass
    
    # 保存最后一个账单
    if current_statement:
        statements.append(current_statement)
    
    return statements


def parse_date(date_str: str):
    """解析日期字符串"""
    if not date_str or date_str.strip() == '':
        return None
    
    date_str = date_str.strip()
    
    # 尝试多种日期格式
    formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%Y/%m/%d',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            continue
    
    return None


def parse_float(value: str):
    """解析浮点数"""
    if not value or value.strip() == '':
        return 0.0
    
    # 移除逗号和空格
    value = value.replace(',', '').replace(' ', '').strip()
    
    try:
        return float(value)
    except:
        return 0.0


def import_csv_to_database(csv_path: str, db: Session = None) -> Dict:
    """
    将CSV数据导入数据库
    
    Args:
        csv_path: CSV文件路径
        db: 数据库会话（可选）
        
    Returns:
        导入结果统计
    """
    if db is None:
        db = SessionLocal()
        should_close = True
    else:
        should_close = False
    
    try:
        # 解析CSV
        statements_data = parse_csv_file(csv_path)
        
        imported_count = 0
        updated_count = 0
        skipped_count = 0
        errors = []
        
        for stmt_data in statements_data:
            try:
                # 检查是否已存在（根据客户名、银行、卡号、账单日期）
                existing = db.query(Statement).filter(
                    Statement.client_name == stmt_data['client_name'],
                    Statement.bank_name == stmt_data['bank_name'],
                    Statement.card_number == stmt_data['card_number'],
                    Statement.statement_date == stmt_data['statement_date']
                ).first()
                
                if existing:
                    # 更新现有记录
                    existing.due_date = stmt_data['due_date']
                    existing.owner_expenses = stmt_data['owner_expenses'] or existing.owner_expenses
                    existing.gz_expenses = stmt_data['gz_expenses'] or existing.gz_expenses
                    existing.owner_os_balance = stmt_data['owner_os_bal'] or existing.owner_os_balance
                    existing.gz_os_balance = stmt_data['gz_os_bal'] or existing.gz_os_balance
                    existing.gz_payment_1 = stmt_data['gz_payment'] or existing.gz_payment_1
                    existing.notes = stmt_data['remarks'] or existing.notes
                    updated_count += 1
                else:
                    # 创建新记录
                    statement = Statement(
                        client_name=stmt_data['client_name'],
                        bank_name=stmt_data['bank_name'],
                        card_number=stmt_data['card_number'],
                        statement_date=stmt_data['statement_date'],
                        due_date=stmt_data['due_date'],
                        owner_expenses=stmt_data['owner_expenses'] or 0.0,
                        gz_expenses=stmt_data['gz_expenses'] or 0.0,
                        owner_os_balance=stmt_data['owner_os_bal'] or 0.0,
                        gz_os_balance=stmt_data['gz_os_bal'] or 0.0,
                        gz_payment_1=stmt_data['gz_payment'] or 0.0,
                        notes=stmt_data['remarks'],
                        verification_status='pending',
                        is_active=True
                    )
                    db.add(statement)
                    imported_count += 1
                
                # 确保客户存在于客户表
                client = db.query(Client).filter(
                    Client.name == stmt_data['client_name']
                ).first()
                
                if not client:
                    client = Client(
                        name=stmt_data['client_name'],
                        default_bank=stmt_data['bank_name'],
                        is_active=True
                    )
                    db.add(client)
                    db.flush()  # 立即提交以获取ID
                
            except Exception as e:
                skipped_count += 1
                errors.append(f"处理 {stmt_data.get('client_name', 'Unknown')} 时出错: {str(e)}")
        
        db.commit()
        
        return {
            'success': True,
            'imported': imported_count,
            'updated': updated_count,
            'skipped': skipped_count,
            'total': len(statements_data),
            'errors': errors
        }
        
    except Exception as e:
        db.rollback()
        return {
            'success': False,
            'error': str(e)
        }
    finally:
        if should_close:
            db.close()


def import_csv_file(csv_path: str) -> Dict:
    """导入CSV文件的便捷函数"""
    if not os.path.exists(csv_path):
        return {
            'success': False,
            'error': f'文件不存在: {csv_path}'
        }
    
    db = SessionLocal()
    try:
        result = import_csv_to_database(csv_path, db)
        return result
    finally:
        db.close()


if __name__ == "__main__":
    # 测试导入
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 csv_importer.py <csv文件路径>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    result = import_csv_file(csv_path)
    
    print("=" * 60)
    print("CSV导入结果")
    print("=" * 60)
    
    if result['success']:
        print(f"✓ 成功导入: {result['imported']} 条")
        print(f"✓ 更新: {result['updated']} 条")
        print(f"✓ 跳过: {result['skipped']} 条")
        print(f"总计: {result['total']} 条")
        
        if result['errors']:
            print("\n错误:")
            for error in result['errors']:
                print(f"  - {error}")
    else:
        print(f"✗ 导入失败: {result.get('error', '未知错误')}")
