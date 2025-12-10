# 🚀 CreditPilot 部署到 Railway 指南

## 🎯 目标

将 CreditPilot 部署到 Railway，获得一个像样的网址（如：creditpilot.railway.app）

---

## 📋 部署步骤

### 第一步：准备 GitHub 仓库

1. **在 GitHub 创建新仓库**
   - 仓库名：`CreditPilot` 或 `creditpilot`

2. **推送代码到 GitHub**
   ```bash
   cd /Users/1491-3913zee/Projects/CreditPilot
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/你的用户名/CreditPilot.git
   git push -u origin main
   ```

### 第二步：在 Railway 部署

1. **访问 Railway**
   - 网址：https://railway.app
   - 用 GitHub 账号登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的 CreditPilot 仓库

3. **Railway 会自动：**
   - 检测到 Python 项目
   - 安装依赖
   - 启动服务
   - 生成域名（如：creditpilot.railway.app）

### 第三步：添加 PostgreSQL 数据库

1. **在 Railway 项目中**
   - 点击 "New" → "Database" → "PostgreSQL"

2. **Railway 会自动：**
   - 创建 PostgreSQL 数据库
   - 生成 `DATABASE_URL` 环境变量

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

**注意：** `DATABASE_URL` 会自动添加（Railway 提供）

### 第五步：配置定时任务

1. **在 Railway 项目中**
   - 点击 "New" → "Cron Job"

2. **设置定时任务：**
   - **Schedule:** `0 22 * * *`（每晚10点）
   - **Command:** `cd backend && python3 reminder_system.py`

---

## 🔧 需要修改的代码

### 1. 修改数据库连接

Railway 会自动提供 PostgreSQL 的 `DATABASE_URL`，代码已经支持（会自动检测）。

### 2. 文件存储

Railway 支持 Volume（持久化存储），可以：
- 在 Railway 项目中添加 Volume
- 挂载到 `/app/uploads` 和 `/app/reports`

---

## ✅ 部署完成后的效果

- ✅ **有像样的网址：** creditpilot.railway.app（或自定义域名）
- ✅ **24小时运行：** 服务器一直在线
- ✅ **自动发送邮件：** 每晚10点自动发送
- ✅ **可以上传单据：** 通过网址访问API
- ✅ **数据持久化：** PostgreSQL 数据库

---

## 🌐 访问方式

部署完成后，可以通过以下方式访问：

- **API文档：** https://creditpilot.railway.app/docs
- **API根路径：** https://creditpilot.railway.app/
- **上传单据：** https://creditpilot.railway.app/api/documents/upload

---

## 💰 费用

**Railway 免费套餐：**
- $5 免费额度/月
- 通常够用（除非流量很大）
- 超出后按使用量付费

---

## 🆘 需要帮助？

如果遇到问题，可以：
1. 查看 Railway 的日志
2. 检查环境变量配置
3. 确认数据库连接

---

**部署完成后，你就有一个像样的网址了！** 🎉
