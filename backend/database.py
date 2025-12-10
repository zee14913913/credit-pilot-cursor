# database.py
# CreditPilot - 数据库初始化

from models import Base, engine
import os

def init_database():
    """初始化数据库，创建所有表"""
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✓ 6个表创建成功")
        print("  - statements (账单表)")
        print("  - transactions (交易记录表)")
        print("  - documents (单据表)")
        print("  - clients (客户表)")
        print("  - reminder_logs (提醒日志表)")
        print("✓ 数据库初始化完成")
        return True
    except Exception as e:
        print(f"✗ 数据库初始化失败: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("CreditPilot 数据库初始化")
    print("=" * 60)
    init_database()
