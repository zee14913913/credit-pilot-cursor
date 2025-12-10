# 🚀 部署到 Railway - 完整指南

## 🎯 目标

将 CreditPilot 部署到 Railway，获得一个像样的网址（如：creditpilot.railway.app）

---

## ✅ 为什么选择 Railway？

1. **完全免费**（有免费额度，通常够用）
2. **部署超简单**（连接GitHub，一键部署）
3. **自动配置**（数据库、域名都自动配置）
4. **支持定时任务**（可以用他们的 Cron Jobs）
5. **有像样的域名**（creditpilot.railway.app）

---

## 📋 完整部署步骤

### 第一步：准备代码并推送到 GitHub

1. **在 GitHub 创建新仓库**
   - 访问：https://github.com/new
   - 仓库名：`CreditPilot` 或 `creditpilot`
   - 选择 Public 或 Private

2. **推送代码到 GitHub**
   ```bash
   cd /Users/1491-3913zee/Projects/CreditPilot
   
   # 初始化 Git（如果还没有）
   git init
   
   # 添加所有文件
   git add .
   
   # 提交
   git commit -m "Initial commit - CreditPilot system"
   
   # 添加远程仓库
   git remote add origin https://github.com/你的用户名/CreditPilot.git
   
   # 推送
   git branch -M main
   git push -u origin main
   ```

### 第二步：在 Railway 部署

1. **访问 Railway**
   - 网址：https://railway.app
   - 点击 "Start a New Project"
   - 用 GitHub 账号登录

2. **部署项目**
   - 点击 "Deploy from GitHub repo"
   - 选择你的 CreditPilot 仓库
   - Railway 会自动检测到 Python 项目

3. **Railway 会自动：**
   - 安装依赖
   - 启动服务
   - 生成域名（如：creditpilot.railway.app）

### 第三步：添加 PostgreSQL 数据库

1. **在 Railway 项目中**
   - 点击 "New" → "Database" → "PostgreSQL"

2. **Railway 会自动：**
   - 创建 PostgreSQL 数据库
   - 生成 `DATABASE_URL` 环境变量
   - 你的代码会自动使用这个数据库

### 第四步：配置环境变量

在 Railway 项目设置 → Variables 中添加：

```env
SENDER_EMAIL=business@infinite-gz.com
SENDER_PASSWORD=gracgnrwghbeocox
RECIPIENT_EMAIL=wang041396@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
UPLOAD_DIR=/app/uploads
REPORTS_DIR=/app/reports
```

**注意：** `DATABASE_URL` 会自动添加（Railway 提供，不需要手动添加）

### 第五步：配置文件存储（Volume）

1. **在 Railway 项目中**
   - 点击 "New" → "Volume"

2. **创建两个 Volume：**
   - `uploads` - 挂载到 `/app/uploads`
   - `reports` - 挂载到 `/app/reports`

3. **这样上传的文件会持久保存**

### 第六步：配置定时任务（每晚10点发送邮件）

1. **在 Railway 项目中**
   - 点击 "New" → "Cron Job"

2. **设置定时任务：**
   - **Name:** `daily-reminder`
   - **Schedule:** `0 22 * * *`（每晚10点，UTC时间）
   - **Command:** `cd backend && python3 reminder_system.py`

**注意：** Railway 使用 UTC 时间，马来西亚时间（UTC+8）的晚上10点 = UTC 下午2点，所以应该设置为 `0 14 * * *`

---

## 🔧 代码调整

### 1. 数据库连接（已支持）

代码已经支持 PostgreSQL，会自动从 `DATABASE_URL` 环境变量读取。

### 2. 文件存储

Railway 的 Volume 会自动挂载，代码不需要修改。

---

## ✅ 部署完成后的效果

- ✅ **有像样的网址：** creditpilot.railway.app
- ✅ **24小时运行：** 服务器一直在线
- ✅ **自动发送邮件：** 每晚10点自动发送
- ✅ **可以上传单据：** 通过网址访问API
- ✅ **数据持久化：** PostgreSQL 数据库
- ✅ **文件持久化：** Volume 存储

---

## 🌐 访问方式

部署完成后，可以通过以下方式访问：

- **API文档：** https://creditpilot.railway.app/docs
- **API根路径：** https://creditpilot.railway.app/
- **上传单据：** https://creditpilot.railway.app/api/documents/upload
- **查看账单：** https://creditpilot.railway.app/api/statements

---

## 📱 小助理如何使用

部署完成后，小助理可以：

1. **访问网址：** https://creditpilot.railway.app/docs
2. **上传单据：** 在API文档页面上传
3. **查看账单：** 通过API查看所有账单
4. **接收邮件：** 每天晚上10点自动收到提醒邮件

---

## 💰 费用

**Railway 免费套餐：**
- $5 免费额度/月
- 通常够用（除非流量很大）
- 超出后按使用量付费（很便宜）

**预计费用：** 免费或 $1-2/月

---

## 🆘 常见问题

### Q1: 部署失败怎么办？

**A:** 查看 Railway 的日志，检查：
- 依赖是否正确安装
- 环境变量是否配置
- 数据库是否连接成功

### Q2: 定时任务不工作？

**A:** 检查：
- Cron Job 的 Schedule 是否正确
- 时区设置（Railway 使用 UTC）
- 命令是否正确

### Q3: 文件上传后丢失？

**A:** 确保创建了 Volume 并正确挂载。

---

## 🎯 下一步

1. **推送代码到 GitHub**
2. **在 Railway 部署**
3. **配置环境变量**
4. **测试功能**
5. **享受有像样的网址！** 🎉

---

**需要我帮你准备部署文件或解决任何问题吗？** 🚀
