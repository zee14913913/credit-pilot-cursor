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
   - OCR识别和验证
   - 自动匹配到交易记录

5. **📅 每晚10点定时提醒（✅ 已完成）**
   - 自动扫描明后天到期账单
   - 计算待付款总金额
   - 识别最紧急客户
   - iPad通知 + Excel日报双重提醒

6. **🖥️ FastAPI后端（✅ 已完成）**
   - RESTful API接口
   - 完整的Dashboard统计
   - PDF上传和解析
   - 单据上传和管理

## 技术栈

- **后端:** Python 3.12, FastAPI, SQLAlchemy, APScheduler
- **数据库:** SQLite (开发), PostgreSQL (生产)
- **PDF处理:** PDFPlumber
- **OCR:** Tesseract
- **前端:** SwiftUI (iPad原生App - 开发中)
- **Excel生成:** Pandas + OpenPyXL

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /home/claude/CreditPilot
pip install -r requirements.txt --break-system-packages
```

### 2. 初始化数据库

```bash
cd backend
python3 database.py
```

### 3. 启动API服务器

```bash
# 开发模式
cd backend
python3 main.py

# 浏览器访问API文档
http://localhost:8000/docs
```

### 4. 启动定时提醒系统

```bash
# 立即测试（不等到晚上10点）
cd backend
python3 reminder_system.py

# 启动定时调度器（每晚10点自动执行）
python3 -c "from reminder_system import setup_scheduler; setup_scheduler()"
```

### 5. 测试API

```bash
cd backend
python3 test_api.py
```

## 📊 提醒系统功能展示

### 每日提醒消息格式：

```
============================================================
📋 CreditPilot 明日到期提醒
============================================================

明天到期 (2025-12-11):
1️⃣ CHANG CHOON CHOW - Alliance Bank *4514
   💰 GZ Pay: RM 1,500.00 ✓ 已付
   📎 单据: 3/3 ✓

后天到期 (2025-12-12):
1️⃣ CHOW KAH FEI - CIMB *4003
   💰 GZ Pay: RM 800.00 ⚠️ 待付款
   💰 Owner Pay: RM 700.00 ⚠️ 待付款

------------------------------------------------------------
总计需代付 (GZ): RM 3,100.00
总计需客户付 (Owner): RM 1,400.00
合计: RM 4,500.00

🔴 最紧急: CHOW KAH FEI (RM 1,500.00)
   原因: GZ需代付 RM 800.00 | Owner需付款 RM 700.00 | 缺少3份单据
============================================================
```

## 🔌 API端点

### Dashboard
- `GET /api/dashboard/stats` - Dashboard统计数据
- `GET /api/dashboard/upcoming` - 未来2天到期账单

### 账单管理
- `POST /api/statements/upload` - 上传PDF账单
- `GET /api/statements` - 获取所有账单
- `GET /api/statements/{id}` - 获取单个账单

### 提醒系统
- `GET /api/reminders/test` - 立即测试提醒
- `GET /api/reminders/daily-report` - 下载Excel日报

完整API文档: `http://localhost:8000/docs`

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

### ⏳ 进行中
- [ ] SwiftUI iPad App界面
- [ ] OCR单据识别

### 📅 计划中
- [ ] 100% PDF验证系统
- [ ] 文件组织系统

## 📚 文档

- [系统建立进度报告](docs/BUILD_PROGRESS.md)
- [iPad App技术架构](docs/IPAD_APP_ARCHITECTURE.md)
- [完整部署指南](docs/DEPLOYMENT_GUIDE.md)

---

**Built with ❤️ for INFINITE GZ**
