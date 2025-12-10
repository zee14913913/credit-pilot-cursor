# classification_engine.py
# CreditPilot - 智能分类引擎（7个Suppliers）

from typing import List, Dict
from decimal import Decimal

# 7个Suppliers（GZ's Expenses）
SUPPLIERS = [
    "PETRONAS",
    "SHELL",
    "CALTEX",
    "BHP",
    "TOLL",
    "PARKING",
    "OTHER"
]

# 关键词匹配规则
SUPPLIER_KEYWORDS = {
    "PETRONAS": ["petronas", "petron", "petrol"],
    "SHELL": ["shell"],
    "CALTEX": ["caltex", "texaco"],
    "BHP": ["bhp"],
    "TOLL": ["toll", "highway", "plus", "nse", "lpt"],
    "PARKING": ["parking", "park", "car park"],
    "OTHER": []  # 默认分类
}


def classify_transaction(description: str, amount: float) -> Dict:
    """
    分类单笔交易
    
    Args:
        description: 交易描述
        amount: 交易金额
        
    Returns:
        {
            "supplier": "供应商名称",
            "is_gz_expense": True/False,
            "is_owner_expense": True/False
        }
    """
    description_lower = description.lower()
    
    # 判断是否为GZ代付（7个Suppliers之一）
    supplier = "OTHER"
    for sup, keywords in SUPPLIER_KEYWORDS.items():
        if any(keyword in description_lower for keyword in keywords):
            supplier = sup
            break
    
    # 如果是7个Suppliers之一，则为GZ代付
    is_gz_expense = supplier != "OTHER"
    is_owner_expense = not is_gz_expense
    
    return {
        "supplier": supplier,
        "is_gz_expense": is_gz_expense,
        "is_owner_expense": is_owner_expense
    }


def calculate_miscellaneous_fee(gz_expenses: float) -> float:
    """
    计算1% Miscellaneous Fee
    
    Args:
        gz_expenses: GZ代付总额
        
    Returns:
        Miscellaneous Fee金额
    """
    if gz_expenses <= 0:
        return 0.0
    
    return round(gz_expenses * 0.01, 2)


def calculate_balances(
    previous_balance: float,
    previous_balance_gz: float,
    owner_expenses: float,
    gz_expenses: float,
    miscellaneous_fee: float,
    owner_payment: float,
    gz_payment_1: float,
    gz_payment_2: float = 0.0
) -> Dict:
    """
    计算余额
    
    公式：
    - Owner's OS Bal = Previous Bal + Owner's Expenses - Owner's Payment + Misc Fee
    - GZ's OS Bal = Previous Bal + GZ's Expenses - GZ's Payment 1
    
    Args:
        previous_balance: 上期余额
        previous_balance_gz: GZ上期余额
        owner_expenses: Owner消费
        gz_expenses: GZ代付消费
        miscellaneous_fee: 1% Miscellaneous Fee
        owner_payment: Owner付款
        gz_payment_1: GZ付款1
        gz_payment_2: GZ付款2（可选）
        
    Returns:
        {
            "owner_os_balance": float,
            "gz_os_balance": float,
            "total_expenses": float
        }
    """
    # Owner's OS Bal = Previous Bal + Owner's Expenses - Owner's Payment + Misc Fee
    owner_os_balance = previous_balance + owner_expenses - owner_payment + miscellaneous_fee
    
    # GZ's OS Bal = Previous Bal + GZ's Expenses - GZ's Payment 1
    gz_os_balance = previous_balance_gz + gz_expenses - gz_payment_1
    
    # 总消费
    total_expenses = owner_expenses + gz_expenses
    
    return {
        "owner_os_balance": round(owner_os_balance, 2),
        "gz_os_balance": round(gz_os_balance, 2),
        "total_expenses": round(total_expenses, 2)
    }


def classify_all_transactions(transactions: List[Dict]) -> Dict:
    """
    分类所有交易并计算总额
    
    Args:
        transactions: 交易列表 [{"description": str, "amount": float, "date": date}, ...]
        
    Returns:
        {
            "owner_expenses": float,
            "gz_expenses": float,
            "transactions": List[Dict]  # 带分类信息的交易列表
        }
    """
    owner_expenses = 0.0
    gz_expenses = 0.0
    classified_transactions = []
    
    for trans in transactions:
        classification = classify_transaction(trans["description"], trans["amount"])
        
        if classification["is_gz_expense"]:
            gz_expenses += trans["amount"]
        else:
            owner_expenses += trans["amount"]
        
        classified_transactions.append({
            **trans,
            **classification
        })
    
    return {
        "owner_expenses": round(owner_expenses, 2),
        "gz_expenses": round(gz_expenses, 2),
        "transactions": classified_transactions
    }
