# init_db.py
# Railway 部署时自动初始化数据库

from models import Base, engine
import os

def init_database():
    """初始化数据库，创建所有表"""
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✓ 数据库表创建成功")
        return True
    except Exception as e:
        print(f"✗ 数据库初始化失败: {e}")
        return False

if __name__ == "__main__":
    print("初始化数据库...")
    init_database()
