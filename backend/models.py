# models.py
# CreditPilot - 数据库模型定义（26个栏位）

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import date
import os

Base = declarative_base()


class Statement(Base):
    """账单表 - 26个栏位"""
    __tablename__ = 'statements'
    
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 客户信息（3个栏位）
    client_name = Column(String(200), nullable=False)  # 客户姓名
    card_number = Column(String(50))  # 卡号（后4位）
    bank_name = Column(String(100))  # 银行名称
    
    # 账单周期（2个栏位）
    statement_date = Column(Date)  # 账单日期
    due_date = Column(Date)  # 到期日
    
    # 上期余额（2个栏位）
    previous_balance = Column(Float, default=0.0)  # 上期余额
    previous_balance_gz = Column(Float, default=0.0)  # GZ上期余额
    
    # 本期消费（4个栏位）
    owner_expenses = Column(Float, default=0.0)  # Owner消费
    gz_expenses = Column(Float, default=0.0)  # GZ代付消费
    total_expenses = Column(Float, default=0.0)  # 总消费
    miscellaneous_fee = Column(Float, default=0.0)  # 1% Miscellaneous Fee
    
    # 本期付款（3个栏位）
    owner_payment = Column(Float, default=0.0)  # Owner付款
    gz_payment_1 = Column(Float, default=0.0)  # GZ付款1
    gz_payment_2 = Column(Float, default=0.0)  # GZ付款2（如果有）
    
    # 本期余额（2个栏位）
    owner_os_balance = Column(Float, default=0.0)  # Owner OS Bal
    gz_os_balance = Column(Float, default=0.0)  # GZ OS Bal
    
    # 验证状态（2个栏位）
    is_verified = Column(Boolean, default=False)  # 是否100%验证通过
    verification_status = Column(String(50), default='pending')  # 验证状态：pending/verified/failed
    
    # 文件信息（3个栏位）
    pdf_path = Column(String(500))  # PDF文件路径
    pdf_filename = Column(String(200))  # PDF文件名
    upload_date = Column(Date, default=lambda: date.today())  # 上传日期
    
    # 其他信息（5个栏位）
    total_transactions = Column(Integer, default=0)  # 交易笔数
    notes = Column(Text)  # 备注
    created_at = Column(Date, default=lambda: date.today())  # 创建时间
    updated_at = Column(Date, default=lambda: date.today(), onupdate=lambda: date.today())  # 更新时间
    is_active = Column(Boolean, default=True)  # 是否激活
    
    # 关系
    transactions = relationship("Transaction", back_populates="statement", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="statement", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Statement(id={self.id}, client={self.client_name}, date={self.statement_date})>"


class Transaction(Base):
    """交易记录表"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    statement_id = Column(Integer, ForeignKey('statements.id'), nullable=False)
    
    # 交易信息
    transaction_date = Column(Date)  # 交易日期
    description = Column(String(500))  # 交易描述
    amount = Column(Float)  # 交易金额
    
    # 分类信息
    supplier = Column(String(100))  # Supplier名称（7个之一）
    is_gz_expense = Column(Boolean, default=False)  # 是否GZ代付
    is_owner_expense = Column(Boolean, default=False)  # 是否Owner消费
    
    # 关系
    statement = relationship("Statement", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, supplier={self.supplier})>"


class Document(Base):
    """单据表（4类单据）"""
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    statement_id = Column(Integer, ForeignKey('statements.id'), nullable=False)
    
    # 单据信息
    document_type = Column(String(50))  # Statement/Merchant Slip/Payment Receipt/Transfer Slip
    file_path = Column(String(500))  # 文件路径
    file_name = Column(String(200))  # 文件名
    
    # OCR信息
    ocr_text = Column(Text)  # OCR识别文本
    ocr_verified = Column(Boolean, default=False)  # OCR是否验证通过
    
    # 匹配信息
    matched_transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=True)
    matched_amount = Column(Float)  # 匹配金额
    
    upload_date = Column(Date, default=lambda: date.today())
    
    # 关系
    statement = relationship("Statement", back_populates="documents")
    
    def __repr__(self):
        return f"<Document(id={self.id}, type={self.document_type})>"


class Client(Base):
    """客户表（52个客户）"""
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=True, nullable=False)  # 客户姓名
    email = Column(String(200))  # 邮箱
    phone = Column(String(50))  # 电话
    
    # 默认设置
    default_bank = Column(String(100))  # 默认银行
    default_card_suffix = Column(String(10))  # 默认卡号后缀
    
    created_at = Column(Date, default=lambda: date.today())
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Client(id={self.id}, name={self.name})>"


class ReminderLog(Base):
    """提醒日志表"""
    __tablename__ = 'reminder_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    reminder_date = Column(Date, default=lambda: date.today())  # 提醒日期
    reminder_time = Column(String(10))  # 提醒时间
    
    # 提醒内容
    tomorrow_count = Column(Integer, default=0)  # 明天到期数量
    day_after_count = Column(Integer, default=0)  # 后天到期数量
    total_gz_payment = Column(Float, default=0.0)  # GZ代付总额
    total_owner_payment = Column(Float, default=0.0)  # Owner付款总额
    most_urgent_client = Column(String(200))  # 最紧急客户
    
    # 报告文件
    excel_report_path = Column(String(500))  # Excel日报路径
    
    created_at = Column(Date, default=lambda: date.today())
    
    def __repr__(self):
        return f"<ReminderLog(id={self.id}, date={self.reminder_date})>"


# 数据库连接
def get_database_url():
    """获取数据库URL"""
    db_url = os.getenv('DATABASE_URL', 'sqlite:///./creditpilot.db')
    
    # Railway PostgreSQL 连接字符串处理
    # Railway 可能使用 postgres://，但 SQLAlchemy 2.0+ 需要 postgresql://
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    return db_url


def create_engine_instance():
    """创建数据库引擎"""
    db_url = get_database_url()
    
    if db_url.startswith('sqlite'):
        return create_engine(db_url, connect_args={"check_same_thread": False})
    else:
        # PostgreSQL 连接配置
        # 添加连接池配置以提高稳定性
        return create_engine(
            db_url,
            pool_pre_ping=True,  # 连接前检查连接是否有效
            pool_recycle=300,    # 回收连接时间（秒）
            echo=False           # 生产环境关闭 SQL 日志
        )


engine = create_engine_instance()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
