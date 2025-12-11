# init_db.py
# Railway 部署时自动初始化数据库

from models import Base, engine
import os
import sys

def init_database():
    """初始化数据库，创建所有表"""
    try:
        # 检查数据库连接
        db_url = os.getenv('DATABASE_URL', '')
        if not db_url:
            print("⚠️  警告: DATABASE_URL 环境变量未设置，使用默认 SQLite")
        else:
            # 隐藏密码显示
            if '@' in db_url:
                display_url = db_url.split('@')[0].split('://')[0] + '://***@' + '@'.join(db_url.split('@')[1:])
            else:
                display_url = db_url
            print(f"📊 数据库连接: {display_url}")
        
        # 创建所有表
        print("🔨 创建数据库表...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ 数据库表创建成功")
        print("  - statements (账单表)")
        print("  - transactions (交易记录表)")
        print("  - documents (单据表)")
        print("  - clients (客户表)")
        print("  - reminder_logs (提醒日志表)")
        print("✅ 数据库初始化完成")
        return True
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        print(f"   错误类型: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("CreditPilot 数据库初始化")
    print("=" * 60)
    success = init_database()
    if not success:
        sys.exit(1)
