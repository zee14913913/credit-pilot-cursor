# 🚀 Railway 部署完整指南

## ✅ 所有文件已准备好！

我已经为你准备好了所有部署文件，现在只需要按照步骤操作即可。

---

## 📋 部署步骤

### 第一步：推送代码到 GitHub

1. **在 GitHub 创建新仓库**
   - 访问：https://github.com/new
   - 仓库名：`CreditPilot` 或 `creditpilot`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"

2. **推送代码到 GitHub**

打开终端，执行以下命令：

```bash
cd /Users/1491-3913zee/Projects/CreditPilot

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit - CreditPilot system ready for Railway"

# 添加远程仓库（替换为你的GitHub用户名）
git remote add origin https://github.com/你的GitHub用户名/CreditPilot.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

**如果遇到问题：**
- 如果提示需要认证，使用 GitHub Personal Access Token
- 或者使用 SSH：`git@github.com:你的用户名/CreditPilot.git`

---

### 第二步：在 Railway 部署

1. **访问 Railway**
   - 网址：https://railway.app
   - 点击 "Start a New Project"
   - 用 GitHub 账号登录（推荐）

2. **部署项目**
   - 点击 "Deploy from GitHub repo"
   - 授权 Railway 访问你的 GitHub（如果第一次）
   - 选择你的 `CreditPilot` 仓库
   - Railway 会自动检测到 Python 项目并开始部署

3. **等待部署完成**
   - Railway 会自动：
     - 安装依赖
     - 启动服务
     - 生成域名（如：creditpilot.railway.app）

---

### 第三步：添加 PostgreSQL 数据库

1. **在 Railway 项目中**
   - 点击 "New" → "Database" → "PostgreSQL"

2. **Railway 会自动：**
   - 创建 PostgreSQL 数据库
   - 生成 `DATABASE_URL` 环境变量
   - 你的代码会自动使用这个数据库

3. **初始化数据库**
   - Railway 部署时会自动运行 `init_db.py`
   - 或者手动运行：在 Railway 的 Terminal 中执行 `python3 backend/init_db.py`

---

### 第四步：配置环境变量

在 Railway 项目设置 → Variables 中添加以下环境变量：

```env
SENDER_EMAIL=business@infinite-gz.com
SENDER_PASSWORD=gracgnrwghbeocox
RECIPIENT_EMAIL=wang041396@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
UPLOAD_DIR=/app/uploads
REPORTS_DIR=/app/reports
```

**添加方法：**
1. 在 Railway 项目中，点击项目名称
2. 点击 "Variables" 标签
3. 点击 "New Variable"
4. 逐个添加上面的环境变量

**注意：** `DATABASE_URL` 会自动添加（Railway 提供，不需要手动添加）

---

### 第五步：配置文件存储（Volume）

1. **在 Railway 项目中**
   - 点击 "New" → "Volume"

2. **创建两个 Volume：**
   - **第一个 Volume：**
     - Name: `uploads`
     - Mount Path: `/app/uploads`
   - **第二个 Volume：**
     - Name: `reports`
     - Mount Path: `/app/reports`

3. **这样上传的文件会持久保存**

---

### 第六步：配置定时任务（每晚10点发送邮件）

**重要：** Railway 使用 UTC 时间，马来西亚时间（UTC+8）的晚上10点 = UTC 下午2点

1. **在 Railway 项目中**
   - 点击 "New" → "Cron Job"

2. **设置定时任务：**
   - **Name:** `daily-reminder`
   - **Schedule:** `0 14 * * *`（UTC 下午2点 = 马来西亚晚上10点）
   - **Command:** `cd backend && python3 reminder_system.py`

3. **保存**

---

## ✅ 部署完成后的检查

### 1. 检查服务是否运行

访问你的 Railway 域名：
- https://你的项目名.railway.app
- 应该看到：`{"name":"CreditPilot API","version":"1.0.0","status":"running","docs":"/docs"}`

### 2. 检查 API 文档

访问：https://你的项目名.railway.app/docs
- 应该看到 Swagger UI 文档页面

### 3. 测试功能

- **查看账单：** https://你的项目名.railway.app/api/statements
- **上传单据：** 在 API 文档页面上传测试
- **测试提醒：** https://你的项目名.railway.app/api/reminders/test

---

## 🌐 访问方式

部署完成后，可以通过以下方式访问：

- **API文档：** https://你的项目名.railway.app/docs
- **API根路径：** https://你的项目名.railway.app/
- **上传单据：** https://你的项目名.railway.app/api/documents/upload
- **查看账单：** https://你的项目名.railway.app/api/statements

---

## 📱 小助理如何使用

部署完成后，小助理可以：

1. **访问网址：** https://你的项目名.railway.app/docs
2. **上传单据：** 在API文档页面上传
3. **查看账单：** 通过API查看所有账单
4. **接收邮件：** 每天晚上10点自动收到提醒邮件

---

## 🔧 如果遇到问题

### 问题1：部署失败

**检查：**
- Railway 日志（在项目页面查看）
- 依赖是否正确安装
- 环境变量是否配置

### 问题2：数据库连接失败

**检查：**
- 是否添加了 PostgreSQL 数据库
- `DATABASE_URL` 环境变量是否存在
- 数据库是否已初始化（运行 `init_db.py`）

### 问题3：定时任务不工作

**检查：**
- Cron Job 的 Schedule 是否正确（`0 14 * * *`）
- 命令是否正确（`cd backend && python3 reminder_system.py`）
- Railway 日志查看执行情况

### 问题4：文件上传后丢失

**检查：**
- 是否创建了 Volume
- Volume 是否正确挂载到 `/app/uploads` 和 `/app/reports`

---

## 💰 费用

**Railway 免费套餐：**
- $5 免费额度/月
- 通常够用（除非流量很大）
- 超出后按使用量付费（很便宜）

**预计费用：** 免费或 $1-2/月

---

## 🎯 完成！

部署完成后，你就有一个像样的网址了！

**需要我帮你检查任何步骤吗？** 🚀
