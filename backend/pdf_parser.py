# pdf_parser.py
# CreditPilot - PDF解析引擎（Alliance Bank）

import pdfplumber
from datetime import datetime
from typing import Dict, List, Optional
import re


def parse_alliance_bank_statement(pdf_path: str) -> Dict:
    """
    解析Alliance Bank信用卡账单PDF
    
    Args:
        pdf_path: PDF文件路径
        
    Returns:
        {
            "client_name": str,
            "card_number": str,
            "bank_name": str,
            "statement_date": date,
            "due_date": date,
            "previous_balance": float,
            "transactions": List[Dict]
        }
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # 提取所有文本
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"
            
            # 解析客户信息
            client_name = extract_client_name(full_text)
            card_number = extract_card_number(full_text)
            
            # 解析账单日期和到期日
            statement_date = extract_statement_date(full_text)
            due_date = extract_due_date(full_text)
            
            # 解析上期余额
            previous_balance = extract_previous_balance(full_text)
            
            # 解析交易记录
            transactions = extract_transactions(pdf)
            
            return {
                "client_name": client_name,
                "card_number": card_number,
                "bank_name": "Alliance Bank",
                "statement_date": statement_date,
                "due_date": due_date,
                "previous_balance": previous_balance,
                "previous_balance_gz": previous_balance,  # 默认相同
                "transactions": transactions
            }
    except Exception as e:
        raise Exception(f"PDF解析失败: {str(e)}")


def extract_client_name(text: str) -> str:
    """提取客户姓名"""
    # 查找常见的客户姓名模式
    patterns = [
        r"Cardholder Name[:\s]+([A-Z\s]+)",
        r"Name[:\s]+([A-Z\s]+)",
        r"Account Holder[:\s]+([A-Z\s]+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return "UNKNOWN"


def extract_card_number(text: str) -> str:
    """提取卡号（后4位）"""
    # 查找卡号模式（通常显示为 **** **** **** 1234）
    patterns = [
        r"\*{4}\s+\*{4}\s+\*{4}\s+(\d{4})",
        r"Card No[:\s]+\*{4}\s+\*{4}\s+\*{4}\s+(\d{4})",
        r"(\d{4})\s*$"  # 最后4位数字
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return "0000"


def extract_statement_date(text: str) -> Optional[datetime]:
    """提取账单日期"""
    # 查找日期模式
    patterns = [
        r"Statement Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_str = match.group(1)
            try:
                # 尝试多种日期格式
                for fmt in ["%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"]:
                    try:
                        return datetime.strptime(date_str, fmt).date()
                    except:
                        continue
            except:
                pass
    
    return None


def extract_due_date(text: str) -> Optional[datetime]:
    """提取到期日"""
    patterns = [
        r"Due Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"Payment Due[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_str = match.group(1)
            try:
                for fmt in ["%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"]:
                    try:
                        return datetime.strptime(date_str, fmt).date()
                    except:
                        continue
            except:
                pass
    
    return None


def extract_previous_balance(text: str) -> float:
    """提取上期余额"""
    patterns = [
        r"Previous Balance[:\s]+RM\s*([\d,]+\.?\d*)",
        r"Opening Balance[:\s]+RM\s*([\d,]+\.?\d*)",
        r"Balance Brought Forward[:\s]+RM\s*([\d,]+\.?\d*)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(",", "")
            try:
                return float(amount_str)
            except:
                pass
    
    return 0.0


def extract_transactions(pdf) -> List[Dict]:
    """提取交易记录"""
    transactions = []
    
    # 尝试从表格中提取交易记录
    for page in pdf.pages:
        tables = page.extract_tables()
        
        for table in tables:
            if not table:
                continue
            
            # 查找表头（通常包含 Date, Description, Amount）
            header_row = None
            for i, row in enumerate(table):
                if row and any(keyword in str(row).lower() for keyword in ["date", "description", "amount", "transaction"]):
                    header_row = i
                    break
            
            if header_row is None:
                continue
            
            # 解析数据行
            for row in table[header_row + 1:]:
                if not row or len(row) < 3:
                    continue
                
                try:
                    # 提取日期
                    date_str = str(row[0]).strip()
                    trans_date = parse_date(date_str)
                    
                    # 提取描述
                    description = str(row[1]).strip() if len(row) > 1 else ""
                    
                    # 提取金额
                    amount_str = str(row[-1]).strip() if row else "0"
                    amount = parse_amount(amount_str)
                    
                    if trans_date and description and amount != 0:
                        transactions.append({
                            "transaction_date": trans_date,
                            "description": description,
                            "amount": amount
                        })
                except Exception as e:
                    continue
    
    return transactions


def parse_date(date_str: str) -> Optional[datetime]:
    """解析日期字符串"""
    if not date_str or date_str.lower() in ["none", "null", ""]:
        return None
    
    # 移除常见的前缀
    date_str = re.sub(r"^\d+\s+", "", date_str)  # 移除行号
    
    # 尝试多种日期格式
    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%Y-%m-%d",
        "%d %b %Y",
        "%d %B %Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except:
            continue
    
    return None


def parse_amount(amount_str: str) -> float:
    """解析金额字符串"""
    if not amount_str:
        return 0.0
    
    # 移除货币符号和空格
    amount_str = re.sub(r"[RM\s,]", "", amount_str, flags=re.IGNORECASE)
    
    # 处理负数（可能显示为括号或负号）
    is_negative = False
    if "(" in amount_str and ")" in amount_str:
        is_negative = True
        amount_str = amount_str.replace("(", "").replace(")", "")
    elif amount_str.startswith("-"):
        is_negative = True
        amount_str = amount_str[1:]
    
    try:
        amount = float(amount_str)
        return -amount if is_negative else amount
    except:
        return 0.0
