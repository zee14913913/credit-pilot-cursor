# CreditPilot - 信用卡账单管理系统

**为INFINITE GZ打造的专业信用卡账单管理解决方案**

## 🎯 系统概述

CreditPilot是一个完整的信用卡账单管理系统，帮助INFINITE GZ管理52个客户的信用卡账单、自动分类消费、计算代付金额，并提供准确的余额追踪。

### 核心功能

1. **自动PDF解析**
   - 上传信用卡账单PDF
   - 自动提取客户信息、账单汇总、交易记录
   - 支持多张share limit卡片

2. **智能分类引擎**
   - 自动识别7个Suppliers（GZ's Expenses）
   - 区分Owner消费 vs GZ代付
   - 计算1% Miscellaneous Fee
   - Owner's Payment vs GZ's Payment智能分类

3. **精确余额计算**
   - Owner's OS Bal = Previous Bal + Owner's Expenses - Owner's Payment + Misc Fee
   - GZ's OS Bal = Previous Bal + GZ's Expenses - GZ's Payment 1
   - 支持负数余额

4. **单据管理**
   - 4类单据：Statement, Merchant Slip, Payment Receipt, Transfer Slip
   - 支持图片和PDF上传
   - 自动关联到账单

5. **📅 每晚10点定时提醒（✅ 已完成）**
   - 自动扫描明后天到期账单
   - 计算待付款总金额
   - 识别最紧急客户
   - 自动发送邮件到 wang041396@gmail.com（带Excel附件）

6. **🖥️ FastAPI后端（✅ 已完成）**
   - RESTful API接口
   - 完整的Dashboard统计
   - PDF上传和解析
   - 单据上传和管理
   - CSV数据导入

## 技术栈

- **后端:** Python 3.12, FastAPI, SQLAlchemy, APScheduler
- **数据库:** SQLite (开发), PostgreSQL (生产)
- **PDF处理:** PDFPlumber
- **OCR:** Tesseract (计划中)
- **前端:** SwiftUI (iPad原生App - 开发中)
- **Excel生成:** Pandas + OpenPyXL
- **部署:** Railway

## 🚀 快速开始

### 本地开发

```bash
# 1. 安装依赖
cd backend
pip install -r requirements.txt

# 2. 初始化数据库
python3 database.py

# 3. 启动API服务器
python3 main.py

# 4. 访问API文档
# http://localhost:8000/docs
```

### 部署到 Railway

详细步骤请查看：[RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md)

## 🔌 API端点

### Dashboard
- `GET /api/dashboard/stats` - Dashboard统计数据
- `GET /api/dashboard/upcoming` - 未来2天到期账单

### 账单管理
- `POST /api/statements/upload` - 上传PDF账单
- `GET /api/statements` - 获取所有账单
- `GET /api/statements/{id}` - 获取单个账单

### 单据管理
- `POST /api/documents/upload` - 上传单据（Merchant Slip / Payment Receipt / Transfer Slip）
- `GET /api/documents` - 获取所有单据
- `GET /api/documents/{id}` - 获取单个单据
- `GET /api/documents/{id}/download` - 下载单据

### 提醒系统
- `GET /api/reminders/test` - 立即测试提醒
- `GET /api/reminders/daily-report` - 下载Excel日报

### 数据导入
- `POST /api/import/csv` - 导入CSV数据

完整API文档: 访问 `/docs` 端点

## 📈 开发状态

### ✅ 已完成
- [x] 数据库模型（26栏位）
- [x] PDF解析引擎（Alliance Bank）
- [x] 自动分类引擎（7 Suppliers）
- [x] 余额计算引擎
- [x] **定时提醒系统（每晚10点）**
- [x] **优先级计算引擎**
- [x] **Excel日报生成**
- [x] **FastAPI后端（完整REST API）**
- [x] **邮件自动发送功能**
- [x] **单据上传功能**
- [x] **CSV数据导入功能**

### ⏳ 进行中
- [ ] SwiftUI iPad App界面
- [ ] OCR单据识别

### 📅 计划中
- [ ] 100% PDF验证系统
- [ ] 文件组织系统

## 📚 文档

- [Railway部署指南](./RAILWAY_DEPLOYMENT.md)
- [部署检查清单](./部署检查清单.md)
- [使用指南](./QUICK_START.md)
- [单据上传说明](./小助理单据上传指南.md)
- [邮件配置说明](./邮件配置完成.md)

---

**Built with ❤️ for INFINITE GZ**
