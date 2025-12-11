# Railway 最终配置指南（完全符合官方文档）

**基于 Railway 官方文档和最新 UI**  
**项目**：CreditPilot  
**GitHub 仓库**：`zee14913913/credit-pilot-cursor`

---

## 📋 配置前准备

### 代码检查 ✅
- ✅ Dockerfile 已存在且正确
- ✅ backend/start.sh 已存在且可执行
- ✅ backend/reminder_system.py 可以独立运行
- ✅ 所有文件路径使用 `/app/uploads` 和 `/app/reports`

---

## 第一步：Postgres 服务配置

### 1.1 创建 Postgres 服务
- 在 Railway 项目主页，点击 **"+Create"**
- 选择 **"DATABASE"** → **"PostgreSQL"**
- Railway 会自动创建并配置

### 1.2 检查 Variables（自动生成）
进入 Postgres 服务 → **Variables**

**Railway 自动生成的变量**（不要修改）：
- `DATABASE_URL`
- `DATABASE_PUBLIC_URL`
- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`

**⚠️ 重要**：这些变量都是自动生成的，**保持原样，不要修改**！

### 1.3 检查 Settings
进入 Postgres 服务 → **Settings**

**确认以下设置**：
- ✅ **Custom Start Command**：**留空**（数据库不需要启动命令）
- ✅ **Cron Schedule**：**留空**（数据库不需要定时任务）
- ✅ **Volume**：**不需要**（数据库不需要挂载 Volume）

**✅ Postgres 服务配置完成**

---

## 第二步：Web 服务配置

### 2.1 创建/检查 Web 服务
- 如果还没有，在 Railway 项目主页，点击 **"+Create"**
- 选择 **"GITHUB REPO"**
- 选择仓库：`zee14913913/credit-pilot-cursor`

### 2.2 Build 设置
进入 Web 服务 → **Settings** → **Build**

**配置**：
- **Builder**：选择 **"Dockerfile"**
- **Dockerfile Path**：填写 `Dockerfile`（如果 Dockerfile 在根目录）
  - 也可以填写 `/Dockerfile`（Railway 会当作根路径）
- **Metal Build Environment**：可以开启 ✅（推荐，更快）

### 2.3 Deploy 设置
进入 Web 服务 → **Settings** → **Deploy**

**配置**：
- **Custom Start Command**：**留空** ✅
  - 使用 Dockerfile 的 CMD：`["bash", "start.sh"]`
  - 或 Procfile 中的命令
- **Cron Schedule**：**留空** ✅
  - 如果使用方案B，Cron 在单独服务中配置

### 2.4 Networking 设置
进入 Web 服务 → **Settings** → **Networking**

**配置**：
- 点击 **"Edit Port"** 或找到端口设置
- 输入：`8000`
- 保存

**确认**：你的应用在容器内部监听 `8000` 端口
- 代码中：`uvicorn main:app --host 0.0.0.0 --port 8000`
- 或：`port = int(os.getenv("PORT", 8000))`

### 2.5 Variables 设置（最关键）

进入 Web 服务 → **Variables**

#### 2.5.1 DATABASE_URL（最重要）⚠️

**操作步骤**：
1. 点击 **"New Variable"** 或查找现有 `DATABASE_URL`
2. **Name**：`DATABASE_URL`
3. **Value**：`${{ Postgres.DATABASE_URL }}`
   - ⚠️ **格式**：双大括号 `{{ }}`，有空格
   - ⚠️ **Postgres**：这是你的数据库服务名称（如果不同，请替换）
   - Railway UI 会自动显示下拉提示，列出可用的服务名称
4. 点击 **"Add"** 或 **"Save"**

**⚠️ 常见错误**：
- ❌ `${Postgres.DATABASE_URL}`（单大括号）
- ❌ `${{Postgres.DATABASE_URL}}`（没有空格）
- ❌ 手动写死的连接字符串（如 `postgresql://user:pass@host/db`）

**✅ 正确格式**：`${{ Postgres.DATABASE_URL }}`

#### 2.5.2 其他必需变量

点击 **"New Variable"**，逐个添加：

| Name | Value | 说明 |
|------|-------|------|
| `SENDER_EMAIL` | `business@infinite-gz.com` | 发件人邮箱 |
| `SENDER_PASSWORD` | `grqcgnrwqhbeocox` | Gmail 应用密码 |
| `RECIPIENT_EMAIL` | `wang041396@gmail.com` | 收件人邮箱 |
| `SMTP_SERVER` | `smtp.gmail.com` | SMTP 服务器 |
| `SMTP_PORT` | `587` | SMTP 端口 |
| `UPLOAD_DIR` | `/app/uploads` | 上传目录 |
| `REPORTS_DIR` | `/app/reports` | 报告目录 |

### 2.6 Volume 挂载

#### 2.6.1 创建 Volume（项目级别）

**⚠️ 重要**：在**项目主页**创建，不是服务页面！

1. 在 Railway **项目主页**（不是服务页面），点击右上角 **"+Create"**
2. 选择 **"VOLUME"**
3. 创建第一个 Volume：
   - **Name**：`uploads`
   - **Mount Path**：`/app/uploads`
   - 点击 **"Add"** 或 **"Create"**
4. 创建第二个 Volume：
   - **Name**：`reports`
   - **Mount Path**：`/app/reports`
   - 点击 **"Add"** 或 **"Create"**

#### 2.6.2 附加 Volume 到 Web 服务

1. 进入 **Web 服务** → **Settings** → **Volumes**
2. 点击 **"Attach Volume"** 或 **"Add Volume"**
3. 选择 `uploads` Volume
4. 确认 **Mount Path** 是 `/app/uploads`
5. 点击 **"Attach"**
6. 重复步骤，附加 `reports` Volume：
   - 选择 `reports` Volume
   - 确认 **Mount Path** 是 `/app/reports`

**✅ Web 服务配置完成**

---

## 第三步：Reminder-Cron 服务配置（方案B - 推荐）

### 3.1 创建 Reminder-Cron 服务

1. 在 Railway 项目主页，点击 **"+Create"**
2. 选择 **"GITHUB REPO"**
3. 选择仓库：`zee14913913/credit-pilot-cursor`（与 Web 服务相同）
4. 点击 **"Deploy"** 或 **"Add"**

### 3.2 重命名服务

1. 点击新创建的服务
2. 进入 **Settings**
3. 找到 **"Service Name"** 或类似选项
4. 改为：`reminder-cron`
5. 保存

### 3.3 Build 设置

进入 Reminder-Cron 服务 → **Settings** → **Build**

**配置**：
- **Builder**：选择 **"Dockerfile"**
- **Dockerfile Path**：填写 `Dockerfile`
- **Metal Build Environment**：可以开启 ✅

### 3.4 Deploy 设置（关键）

进入 Reminder-Cron 服务 → **Settings** → **Deploy**

**配置**：
- **Custom Start Command**：填写
  ```
  cd backend && python3 reminder_system.py
  ```
- **Cron Schedule**：找到 **"Cron Schedule"** 部分
  - 点击 **"Add Schedule"** 或直接在输入框中输入
  - 输入：`0 14 * * *`
    - 这表示每天 UTC 14:00（马来西亚时间 22:00）执行
  - 保存

**⚠️ 重要**：
- Cron 是绑定服务的 Start Command 来运行的
- 不是项目级别的独立 "Cron Job" 任务（这是旧做法）
- 命令由该服务自身的 Start Command 控制

### 3.5 Variables 设置

进入 Reminder-Cron 服务 → **Variables**

**添加以下变量**（与 Web 服务相同）：

| Name | Value |
|------|-------|
| `DATABASE_URL` | `${{ Postgres.DATABASE_URL }}` ⚠️ **关键** |
| `SENDER_EMAIL` | `business@infinite-gz.com` |
| `SENDER_PASSWORD` | `grqcgnrwqhbeocox` |
| `RECIPIENT_EMAIL` | `wang041396@gmail.com` |
| `SMTP_SERVER` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `UPLOAD_DIR` | `/app/uploads` |
| `REPORTS_DIR` | `/app/reports` |

### 3.6 Volume 挂载（如果需要）

如果 `reminder_system.py` 需要读取/写入文件：

1. 进入 Reminder-Cron 服务 → **Settings** → **Volumes**
2. 点击 **"Attach Volume"**
3. 选择 `reports` Volume（用于保存生成的 Excel 报告）
4. 确认 **Mount Path** 是 `/app/reports`
5. 点击 **"Attach"**

**✅ Reminder-Cron 服务配置完成**

---

## 第四步：验证和测试

### 4.1 快速检查清单

#### Postgres 服务
- [ ] Variables 中有 `DATABASE_URL`（自动生成，未修改）
- [ ] Settings 中 Start Command 和 Cron Schedule 都留空

#### Web 服务
- [ ] Build → Builder = `Dockerfile`
- [ ] Deploy → Start Command = **留空**
- [ ] Deploy → Cron Schedule = **留空**（如果使用方案B）
- [ ] Networking → Port = `8000`
- [ ] Variables → `DATABASE_URL` = `${{ Postgres.DATABASE_URL }}` ⚠️ **关键**
- [ ] Variables → 所有其他变量已设置
- [ ] Volumes → `uploads` 和 `reports` 已挂载

#### Reminder-Cron 服务（方案B）
- [ ] Build → Builder = `Dockerfile`
- [ ] Deploy → Start Command = `cd backend && python3 reminder_system.py`
- [ ] Deploy → Cron Schedule = `0 14 * * *`
- [ ] Variables → `DATABASE_URL` = `${{ Postgres.DATABASE_URL }}`
- [ ] Variables → 所有其他变量已设置
- [ ] Volumes → `reports` 已挂载（如果需要）

#### Volume（项目级别）
- [ ] 已创建 `uploads` Volume，Mount Path = `/app/uploads`
- [ ] 已创建 `reports` Volume，Mount Path = `/app/reports`
- [ ] 已附加到相应服务

### 4.2 测试数据库连接

1. 进入 **Web 服务** → **Shell** 或 **Terminal**
2. 执行：
   ```bash
   cd backend && python3 init_db.py
   ```
3. **预期结果**：
   - ✅ 无错误输出
   - ✅ 显示 "✅ 数据库表创建成功"
   - ✅ 显示 "✅ 数据库初始化完成"

**如果失败**：
- 检查 `DATABASE_URL` 变量格式：`${{ Postgres.DATABASE_URL }}`
- 检查 Postgres 服务名称是否正确
- 检查 Postgres 服务是否正在运行

### 4.3 测试 Web 服务

1. 获取 Web 服务的公共 URL
   - 在 Web 服务 → **Networking** → **Public Networking**
   - 点击 **"Generate Domain"** 或查看已有域名

2. 访问健康检查端点：
   ```bash
   curl https://your-app.railway.app/health
   ```
   或直接在浏览器访问：
   ```
   https://your-app.railway.app/health
   ```

3. **预期结果**：
   - ✅ 返回 `{"status": "healthy"}` 或类似 JSON
   - ✅ HTTP 状态码 200

### 4.4 测试 Cron 服务（方案B）

1. 进入 **Reminder-Cron 服务** → **Deployments** 或 **Logs**
2. 等待到 UTC 14:00 或手动触发一次部署来测试

**预期结果**：
- ✅ 服务在 Cron 时间启动
- ✅ 执行 `reminder_system.py`
- ✅ 生成 Excel 报告
- ✅ 发送邮件（检查收件箱）
- ✅ 日志中无错误

---

## ⚠️ 关键配置点总结

### 1. DATABASE_URL 格式（最重要）
```
✅ 正确：${{ Postgres.DATABASE_URL }}
❌ 错误：${Postgres.DATABASE_URL}（单大括号）
❌ 错误：${{Postgres.DATABASE_URL}}（没有空格）
❌ 错误：手动写死的连接字符串
```

### 2. Cron 配置位置
```
✅ 正确：服务的 Settings → Deploy → Cron Schedule
❌ 错误：项目级别的 "Cron Job"（旧做法）
```

### 3. Volume 创建位置
```
✅ 正确：项目级别创建（项目主页的 "+Create" → "VOLUME"）
❌ 错误：服务级别创建
```

### 4. Start Command
```
✅ Web 服务：留空（使用 Dockerfile CMD）
✅ Reminder-Cron 服务：cd backend && python3 reminder_system.py
```

---

## 📚 参考文档

- [Railway Variables Guide](https://docs.railway.com/guides/variables)
- [Railway Cron Jobs Guide](https://docs.railway.com/guides/cron-jobs)
- [Railway PostgreSQL Guide](https://docs.railway.com/guides/postgresql)
- [Railway Volume Guide](https://docs.railway.com/guides/build-a-database-service)

---

## ✅ 完成！

如果所有检查都通过，你的 CreditPilot 系统应该可以顺利运行！

**配置完成时间**：2025-12-10  
**符合 Railway 官方文档**：✅ 是
