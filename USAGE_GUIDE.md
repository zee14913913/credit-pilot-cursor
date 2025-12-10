# CreditPilot 使用指南

## 📍 在哪里使用？

### 当前可用方式：

1. **浏览器访问API文档**（推荐新手）
   - 启动服务器后，在浏览器打开：`http://localhost:8000/docs`
   - 可以直接在网页上测试所有API功能
   - 支持上传PDF、查看账单等

2. **命令行/终端**
   - 使用 `curl` 命令调用API
   - 使用 `test_api.py` 脚本测试

3. **iPad App**（开发中）
   - 目前还在开发阶段
   - 完成后可以在iPad上直接使用

---

## 🚀 如何使用？

### 第一步：启动后端服务器

```bash
# 1. 进入项目目录
cd /Users/1491-3913zee/Projects/CreditPilot/backend

# 2. 安装依赖（首次使用）
pip install -r requirements.txt

# 3. 初始化数据库（首次使用）
python3 database.py

# 4. 启动API服务器
python3 main.py
```

**成功启动后，你会看到：**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 第二步：访问API文档（最简单的方式）

1. **打开浏览器**
2. **访问：** `http://localhost:8000/docs`
3. **你会看到一个交互式API文档页面**（Swagger UI）

### 第三步：测试功能

#### 方式1：在浏览器API文档中测试

1. **查看Dashboard统计**
   - 点击 `GET /api/dashboard/stats`
   - 点击 "Try it out" → "Execute"
   - 查看返回的统计数据

2. **上传PDF账单**
   - 点击 `POST /api/statements/upload`
   - 点击 "Try it out"
   - 点击 "Choose File" 选择PDF文件
   - 点击 "Execute"
   - 系统会自动解析PDF并创建账单记录

3. **查看所有账单**
   - 点击 `GET /api/statements`
   - 点击 "Try it out" → "Execute"
   - 查看所有已上传的账单

4. **测试提醒系统**
   - 点击 `GET /api/reminders/test`
   - 点击 "Try it out" → "Execute"
   - 查看提醒消息

#### 方式2：使用命令行测试

```bash
# 测试API是否运行
curl http://localhost:8000/

# 查看Dashboard统计
curl http://localhost:8000/api/dashboard/stats

# 查看未来2天到期账单
curl http://localhost:8000/api/dashboard/upcoming

# 运行完整测试脚本
cd backend
python3 test_api.py
```

#### 方式3：上传PDF账单（命令行）

```bash
# 上传PDF文件
curl -X POST "http://localhost:8000/api/statements/upload" \
  -F "file=@/path/to/your/statement.pdf"
```

---

## 🔔 提醒系统说明

### 当前提醒形式（已实现）

#### 1. **控制台输出**（终端显示）
当提醒系统运行时，会在终端打印详细的提醒消息：

```
============================================================
📋 CreditPilot 明日到期提醒
============================================================

明天到期 (2025-01-28):
1️⃣ CHANG CHOON CHOW - Alliance Bank *4514
   💰 GZ Pay: RM 1,500.00 ✓ 已付
   💰 Owner Pay: RM 0.00 ⚠️ 待付款
   📎 单据: 3/3 ✓

后天到期 (2025-01-29):
1️⃣ CHOW KAH FEI - CIMB *4003
   💰 GZ Pay: RM 800.00 ⚠️ 待付款
   💰 Owner Pay: RM 700.00 ⚠️ 待付款
   📎 单据: 1/3 ⚠️

------------------------------------------------------------
总计需代付 (GZ): RM 2,300.00
总计需客户付 (Owner): RM 700.00
合计: RM 3,000.00

🔴 最紧急: CHOW KAH FEI (RM 1,500.00)
   原因: GZ需代付 RM 800.00 | Owner需付款 RM 700.00 | 缺少2份单据
============================================================
```

#### 2. **Excel日报文件**
系统会自动生成Excel文件，保存在：
```
/Users/1491-3913zee/Projects/CreditPilot/reports/
CreditPilot_Daily_Report_YYYYMMDD.xlsx
```

Excel文件包含：
- 明天到期的账单列表
- 后天到期的账单列表
- 总计金额
- 最紧急客户信息

#### 3. **API端点获取提醒**
可以通过API获取提醒数据：
```bash
# 获取提醒信息（JSON格式）
curl http://localhost:8000/api/reminders/test

# 下载Excel日报
curl -O http://localhost:8000/api/reminders/daily-report
```

### 定时提醒（每晚10点）

#### 方式1：立即测试（不等到晚上10点）
```bash
cd backend
python3 reminder_system.py
```

#### 方式2：启动定时调度器（后台运行）
```bash
cd backend
python3 -c "from reminder_system import setup_scheduler; setup_scheduler()"
```

**注意：** 这个命令会一直运行，直到你按 `Ctrl+C` 停止。

#### 方式3：使用systemd服务（Linux服务器）
参考 `docs/DEPLOYMENT_GUIDE.md` 中的systemd配置。

### 未来提醒形式（iPad App开发完成后）

1. **iPad本地通知**
   - 每晚10点自动弹出通知
   - 显示提醒消息摘要
   - 点击通知直接打开App查看详情

2. **App内提醒**
   - Dashboard页面显示红色提醒角标
   - 专门的提醒页面展示详细信息

---

## 📱 完整使用流程示例

### 场景：上传一张新的信用卡账单

```bash
# 1. 确保服务器正在运行
cd /Users/1491-3913zee/Projects/CreditPilot/backend
python3 main.py

# 2. 在另一个终端窗口，上传PDF
curl -X POST "http://localhost:8000/api/statements/upload" \
  -F "file=@/Users/你的用户名/Downloads/statement.pdf"

# 3. 查看解析结果
# 系统会返回JSON，包含：
# - 客户姓名
# - 账单日期
# - 交易笔数
# - 自动分类结果（Owner消费 vs GZ代付）
# - 计算的余额

# 4. 查看账单详情
curl http://localhost:8000/api/statements/1

# 5. 查看Dashboard统计
curl http://localhost:8000/api/dashboard/stats
```

### 场景：查看明日到期提醒

```bash
# 方法1：通过API获取
curl http://localhost:8000/api/dashboard/upcoming

# 方法2：运行提醒系统（会打印详细消息）
cd backend
python3 reminder_system.py

# 方法3：下载Excel日报
curl -O http://localhost:8000/api/reminders/daily-report
```

---

## 🖥️ 推荐使用方式

### 对于日常使用：

1. **启动服务器**（保持运行）
   ```bash
   cd backend
   python3 main.py
   ```

2. **打开浏览器访问API文档**
   - 地址：`http://localhost:8000/docs`
   - 这是最直观、最简单的方式

3. **上传PDF账单**
   - 在API文档页面直接上传
   - 立即看到解析结果

4. **查看提醒**
   - 访问 `/api/dashboard/upcoming` 查看未来2天到期账单
   - 或运行 `reminder_system.py` 获取详细提醒

### 对于自动化使用：

1. **设置定时提醒**（每晚10点）
   ```bash
   # 使用systemd或cron（参考部署指南）
   ```

2. **自动生成Excel日报**
   - 系统会自动保存到 `reports/` 目录
   - 可以通过API下载

---

## ❓ 常见问题

### Q1: 服务器启动失败？
- 检查是否已安装依赖：`pip install -r requirements.txt`
- 检查端口8000是否被占用

### Q2: 上传PDF后没有反应？
- 检查PDF是否是Alliance Bank的账单格式
- 查看终端错误信息
- 检查 `uploads/` 目录是否有文件

### Q3: 提醒没有显示？
- 确保数据库中有账单数据
- 确保账单的 `due_date` 是明天或后天
- 运行 `python3 reminder_system.py` 测试

### Q4: 如何查看日志？
- API日志在终端输出
- 提醒日志保存在数据库中（ReminderLog表）

---

## 📞 需要帮助？

- 查看完整文档：`docs/DEPLOYMENT_GUIDE.md`
- 查看API文档：`http://localhost:8000/docs`
- 查看项目状态：`PROJECT_STATUS.md`
