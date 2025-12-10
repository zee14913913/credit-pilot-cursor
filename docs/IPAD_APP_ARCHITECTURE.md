# CreditPilot iPad原生App技术架构

## 技术栈选择

### 前端框架：SwiftUI
**优势：**
- 原生性能最佳
- iPad特性完美支持（多任务、Split View、Pencil）
- 与iOS生态系统深度集成
- 本地通知（每晚10点提醒）
- 文件系统访问（PDF上传）
- 相机调用（单据拍照）

### 后端：FastAPI (Python)
**优势：**
- 已有的PDF解析、分类引擎可直接使用
- 快速开发RESTful API
- 自动生成API文档
- 异步处理PDF和OCR

### 数据库：PostgreSQL (生产) / SQLite (开发)
**当前使用：** SQLite（开发阶段）  
**生产部署：** PostgreSQL（更强大的并发支持）

### OCR服务：Tesseract
**优势：**
- 免费开源
- 支持中文和英文
- 可本地部署
- 适合处理结构化表格（账单、单据）

---

## App架构设计

### 1. 三层架构

```
┌─────────────────────────────────────┐
│          SwiftUI Frontend           │
│     (iPad Native App - Views)       │
└──────────────┬──────────────────────┘
               │ HTTP/REST API
┌──────────────▼──────────────────────┐
│         FastAPI Backend             │
│  (PDF Parser + Classification)      │
└──────────────┬──────────────────────┘
               │ SQLAlchemy ORM
┌──────────────▼──────────────────────┐
│      PostgreSQL Database            │
│    (26 Fields + Transactions)       │
└─────────────────────────────────────┘
```

### 2. App页面结构

```
CreditPilot.app/
│
├── 登录页 (LoginView)
│   └── 输入小旺管理员密码
│
├── Dashboard总览 (DashboardView)
│   ├── 顶部：未来2天到期提醒
│   ├── 客户列表（52个）
│   │   ├── 按到期日排序
│   │   ├── 筛选：银行/日期/状态
│   │   └── 搜索功能
│   └── 底部Tabbar
│
├── 客户详情 (ClientDetailView)
│   ├── 客户信息
│   ├── 所有信用卡列表
│   └── 按银行分组
│
├── 月份卡片 (StatementDetailView)
│   ├── 顶部：PDF预览
│   │   ├── 可翻页
│   │   ├── 可缩放
│   │   └── 可标注
│   ├── 中间：验证状态
│   │   ├── ✓ 100%验证通过
│   │   ├── ⚠️ 待验证（差异X处）
│   │   └── ⊗ 验证失败
│   ├── 底部：账单表格
│   │   ├── 26个栏位完整显示
│   │   ├── 可编辑（手动修正）
│   │   └── 自动保存
│   └── 单据上传区
│       ├── Merchant Slip
│       ├── Payment Receipt
│       └── Transfer Slip
│
├── 上传页面 (UploadView)
│   ├── 拍照上传
│   ├── 相册选择
│   ├── PDF文件选择
│   ├── OCR识别进度
│   └── 验证结果
│
├── 提醒设置 (ReminderSettingsView)
│   ├── 提醒时间（默认22:00）
│   ├── 提醒方式
│   │   ├── iPad通知
│   │   └── Excel日报
│   └── 通知测试
│
└── 设置页 (SettingsView)
    ├── 账号管理
    ├── 数据同步
    ├── 导出Excel
    └── 关于
```

### 3. 核心功能模块

#### A. PDF上传与解析
```swift
// PDFUploadManager.swift
class PDFUploadManager {
    func uploadPDF(_ file: URL) async throws -> Statement
    func verifyParsing(_ statementId: Int) async throws -> VerificationResult
    func applyCorrection(_ correction: Correction) async throws
}
```

#### B. 自动分类
```swift
// ClassificationEngine.swift
class ClassificationEngine {
    func classifyTransaction(_ transaction: Transaction) -> Classification
    func calculateMiscellaneousFee(_ gzExpenses: Decimal) -> Decimal
    func calculateBalances(_ statement: Statement) -> Balances
}
```

#### C. 单据OCR识别
```swift
// OCRService.swift
class OCRService {
    func recognizeMerchantSlip(_ image: UIImage) async throws -> MerchantSlipData
    func recognizePaymentReceipt(_ image: UIImage) async throws -> PaymentData
    func recognizeTransferSlip(_ image: UIImage) async throws -> TransferData
}
```

#### D. 本地通知
```swift
// NotificationManager.swift
class NotificationManager {
    func scheduleDaily10PMReminder()
    func sendReminder(_ message: String, priority: NotificationPriority)
    func requestPermission()
}
```

---

## 数据流

### 1. PDF上传流程
```
1. 用户在iPad选择PDF文件
   ↓
2. SwiftUI调用API: POST /api/statements/upload
   ↓
3. FastAPI接收文件，调用pdf_parser.py
   ↓
4. 解析客户信息、账单汇总、交易记录
   ↓
5. 调用classification_engine.py自动分类
   ↓
6. 返回解析结果 + 验证状态
   ↓
7. SwiftUI显示验证界面
   - 逐行对比（原始PDF vs 生成表格）
   - 差异高亮
   - 允许手动修正
   ↓
8. 用户确认"✓ 100%验证通过"
   ↓
9. 保存到数据库
```

### 2. 单据上传流程
```
1. 用户拍照或选择图片
   ↓
2. SwiftUI调用API: POST /api/documents/upload
   ↓
3. FastAPI接收图片，调用Tesseract OCR
   ↓
4. 识别文本和结构化数据
   - Merchant Slip: 商家名称、金额、日期
   - Payment Receipt: 付款金额、日期、付款人
   - Transfer Slip: 转账金额、账户、编号
   ↓
5. 自动匹配到对应交易记录
   ↓
6. 交叉验证金额
   ↓
7. 返回识别结果
   ↓
8. SwiftUI显示验证界面
   - OCR识别文本
   - 匹配的交易记录
   - 验证状态（✓ / ⚠️）
   ↓
9. 用户确认或修正
   ↓
10. 保存到数据库
```

### 3. 每日提醒流程
```
1. 系统定时器（每晚22:00）
   ↓
2. Python调度器触发reminder_system.py
   ↓
3. 查询数据库：未来2天到期账单
   ↓
4. 计算优先级（GZ代付 > Owner付款 > 单据缺失）
   ↓
5. 生成提醒消息
   ↓
6. 发送iPad本地通知
   ↓
7. 生成Excel日报并保存
```

---

## API端点设计

### 账单管理
```
POST   /api/statements/upload          上传PDF账单
GET    /api/statements                 获取所有账单
GET    /api/statements/{id}            获取单个账单
PUT    /api/statements/{id}            更新账单
DELETE /api/statements/{id}            删除账单
POST   /api/statements/{id}/verify     验证账单
```

### 交易管理
```
GET    /api/statements/{id}/transactions    获取账单交易
POST   /api/transactions/classify           自动分类交易
PUT    /api/transactions/{id}               修正分类
```

### 单据管理
```
POST   /api/documents/upload               上传单据
POST   /api/documents/ocr                  OCR识别
GET    /api/documents/{id}                 获取单据
DELETE /api/documents/{id}                 删除单据
```

### Dashboard
```
GET    /api/dashboard                      Dashboard数据
GET    /api/dashboard/upcoming             未来2天到期
GET    /api/dashboard/statistics           统计数据
```

### 提醒
```
GET    /api/reminders                      获取提醒
POST   /api/reminders/test                 测试提醒
GET    /api/reminders/daily-report         下载Excel日报
```

---

## 开发步骤

### Phase 1: FastAPI后端 (3-4天)
- [ ] 设置FastAPI项目结构
- [ ] 实现所有API端点
- [ ] 集成已有的PDF解析器和分类引擎
- [ ] 集成Tesseract OCR
- [ ] API文档（自动生成）
- [ ] 单元测试

### Phase 2: SwiftUI基础界面 (4-5天)
- [ ] Xcode项目初始化
- [ ] 数据模型（Codable）
- [ ] API客户端（URLSession + Combine）
- [ ] 基础UI组件库
  - [ ] 卡片视图
  - [ ] 列表视图
  - [ ] 表格视图
  - [ ] PDF预览器

### Phase 3: 核心功能 (5-7天)
- [ ] Dashboard总览页
- [ ] PDF上传与验证界面
- [ ] 100%验证流程
- [ ] 单据拍照上传
- [ ] OCR识别与验证
- [ ] 手动编辑功能

### Phase 4: 提醒系统 (2-3天)
- [ ] 本地通知权限
- [ ] 每晚10点定时提醒
- [ ] 提醒消息生成
- [ ] Excel日报下载
- [ ] 提醒设置页面

### Phase 5: 优化与测试 (3-4天)
- [ ] UI/UX优化
- [ ] 性能优化
- [ ] 错误处理
- [ ] 离线支持
- [ ] 用户测试
- [ ] Bug修复

**预计总开发时间：** 17-23天

---

## 部署方案

### 开发环境
```
Mac/MacBook (Xcode)
├── SwiftUI App开发
├── iOS Simulator测试
└── 实体iPad测试

Server (本地或Cloud)
├── FastAPI (uvicorn)
├── PostgreSQL
└── Tesseract OCR
```

### 生产环境选项

#### 选项A：本地服务器（推荐）
```
优势：
- 数据完全本地，安全性高
- 无云端费用
- 响应速度快

需求：
- 一台24/7运行的Mac或Linux服务器
- 固定IP或动态DNS
- FastAPI + PostgreSQL + Tesseract
```

#### 选项B：云端部署
```
优势：
- 随时随地访问
- 自动备份
- 可扩展性强

推荐服务：
- DigitalOcean (RM 20-40/月)
- AWS Lightsail (RM 15-30/月)
- Azure App Service (RM 20-50/月)
```

---

## 安全考虑

### 1. 认证授权
- 小旺管理员密码登录
- JWT Token认证
- API密钥

### 2. 数据加密
- HTTPS通信（SSL/TLS）
- 数据库加密（敏感字段）
- 本地存储加密

### 3. 隐私保护
- 客户数据脱敏
- 单据图片水印
- 访问日志

---

## 后续扩展

### 可能的功能扩展
- [ ] 多用户支持（不同管理员）
- [ ] 数据导出（Excel/CSV）
- [ ] 历史数据分析
- [ ] 图表统计
- [ ] 自动催款提醒
- [ ] 与银行API集成
- [ ] Apple Watch快速查看

---

**技术栈总结：**
- **前端：** SwiftUI (iPad原生)
- **后端：** FastAPI (Python)
- **数据库：** PostgreSQL / SQLite
- **OCR：** Tesseract
- **提醒：** APScheduler + iOS Local Notification
- **部署：** 本地服务器 / Cloud VPS
