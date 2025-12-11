# Railway 配置验证指南

**项目**：CreditPilot  
**GitHub 仓库**：`zee14913913/credit-pilot-cursor`  
**检查日期**：2025-12-10

---

## 📋 Railway 配置检查清单

### 第一步：Postgres 服务检查

#### 1.1 服务存在性
- [ ] 在 Railway 项目中有 Postgres 服务
- [ ] 服务名称是 `Postgres`（或记住实际名称）

#### 1.2 Variables 检查
进入 Postgres 服务 → Variables，确认：

- [ ] `DATABASE_URL` 存在（Railway 自动生成）
- [ ] `DATABASE_PUBLIC_URL` 存在（Railway 自动生成）
- [ ] `PGHOST` 存在
- [ ] `PGPORT` 存在
- [ ] `PGUSER` 存在
- [ ] `PGPASSWORD` 存在
- [ ] `PGDATABASE` 存在

**⚠️ 重要**：这些变量都是 Railway 自动生成的，**不要修改**！

#### 1.3 Settings 检查
进入 Postgres 服务 → Settings，确认：

- [ ] **Custom Start Command**：留空（数据库不需要启动命令）
- [ ] **Cron Schedule**：留空（数据库不需要定时任务）
- [ ] **Volume**：不需要挂载

**✅ Postgres 服务检查完成**

---

### 第二步：Web 服务检查

#### 2.1 服务存在性
- [ ] 在 Railway 项目中有 Web 服务
- [ ] 服务名称是 `web` 或类似名称

#### 2.2 Build 设置检查
进入 Web 服务 → Settings → Build：

- [ ] **Builder**：选择 `Dockerfile`
- [ ] **Dockerfile Path**：填写 `Dockerfile`（如果 Dockerfile 在根目录）
- [ ] **Metal Build Environment**：可以开启 ✅（推荐，更快）

#### 2.3 Deploy 设置检查
进入 Web 服务 → Settings → Deploy：

- [ ] **Custom Start Command**：**留空**（使用 Dockerfile 的 CMD）
- [ ] **Cron Schedule**：**留空**（如果使用方案B，Cron 在单独服务中）

#### 2.4 Networking 设置检查
进入 Web 服务 → Settings → Networking：

- [ ] **Port**：设置为 `8000`
  - 如果显示 "Edit Port"，点击并输入 `8000`
  - 确认应用在容器内监听 `8000` 端口

#### 2.5 Variables 检查（最关键）
进入 Web 服务 → Variables，逐一检查：

**必需变量列表：**

| 变量名 | 值 | 检查 |
|--------|-----|------|
| `DATABASE_URL` | `${{ Postgres.DATABASE_URL }}` | [ ] ⚠️ **最重要** |
| `SENDER_EMAIL` | `business@infinite-gz.com` | [ ] |
| `SENDER_PASSWORD` | `grqcgnrwqhbeocox` | [ ] |
| `RECIPIENT_EMAIL` | `wang041396@gmail.com` | [ ] |
| `SMTP_SERVER` | `smtp.gmail.com` | [ ] |
| `SMTP_PORT` | `587` | [ ] |
| `UPLOAD_DIR` | `/app/uploads` | [ ] |
| `REPORTS_DIR` | `/app/reports` | [ ] |

**⚠️ DATABASE_URL 格式检查：**
- ✅ 正确：`${{ Postgres.DATABASE_URL }}`（双大括号，有空格）
- ❌ 错误：`${Postgres.DATABASE_URL}`（单大括号）
- ❌ 错误：`${{Postgres.DATABASE_URL}}`（没有空格）
- ❌ 错误：手动写死的连接字符串

**如果 DATABASE_URL 不存在或格式错误：**
1. 点击 "New Variable"
2. Name：`DATABASE_URL`
3. Value：`${{ Postgres.DATABASE_URL }}`
   - Railway UI 会自动显示下拉提示，选择 Postgres 服务
4. 点击 "Add"

#### 2.6 Volume 挂载检查
进入 Web 服务 → Settings → Volumes：

- [ ] `uploads` Volume 已挂载
  - Mount Path：`/app/uploads`
- [ ] `reports` Volume 已挂载
  - Mount Path：`/app/reports`

**如果 Volume 未挂载：**
1. 点击 "Attach Volume"
2. 选择 `uploads` Volume
3. 确认 Mount Path 是 `/app/uploads`
4. 重复步骤挂载 `reports` Volume

**✅ Web 服务检查完成**

---

### 第三步：Reminder-Cron 服务检查（方案B）

#### 3.1 服务存在性
- [ ] 在 Railway 项目中有 Reminder-Cron 服务
- [ ] 服务名称是 `reminder-cron` 或类似名称

#### 3.2 Build 设置检查
进入 Reminder-Cron 服务 → Settings → Build：

- [ ] **Builder**：选择 `Dockerfile`
- [ ] **Dockerfile Path**：填写 `Dockerfile`
- [ ] **Metal Build Environment**：可以开启 ✅

#### 3.3 Deploy 设置检查（关键）
进入 Reminder-Cron 服务 → Settings → Deploy：

- [ ] **Custom Start Command**：填写
  ```
  cd backend && python3 reminder_system.py
  ```
- [ ] **Cron Schedule**：填写
  ```
  0 14 * * *
  ```
  - 这表示每天 UTC 14:00（马来西亚时间 22:00）执行

#### 3.4 Variables 检查
进入 Reminder-Cron 服务 → Variables：

- [ ] `DATABASE_URL` = `${{ Postgres.DATABASE_URL }}` ⚠️ **关键**
- [ ] `SENDER_EMAIL` = `business@infinite-gz.com`
- [ ] `SENDER_PASSWORD` = `grqcgnrwqhbeocox`
- [ ] `RECIPIENT_EMAIL` = `wang041396@gmail.com`
- [ ] `SMTP_SERVER` = `smtp.gmail.com`
- [ ] `SMTP_PORT` = `587`
- [ ] `UPLOAD_DIR` = `/app/uploads`
- [ ] `REPORTS_DIR` = `/app/reports`

**所有变量应该与 Web 服务相同**

#### 3.5 Volume 挂载检查
进入 Reminder-Cron 服务 → Settings → Volumes：

- [ ] `reports` Volume 已挂载（如果需要保存 Excel 报告）
  - Mount Path：`/app/reports`

**✅ Reminder-Cron 服务检查完成**

---

### 第四步：Volume 检查（项目级别）

#### 4.1 Volume 创建检查
在 Railway 项目主页（不是服务页面），检查：

- [ ] 已创建 Volume：`uploads`
  - Mount Path：`/app/uploads`
- [ ] 已创建 Volume：`reports`
  - Mount Path：`/app/reports`

**如果 Volume 不存在：**
1. 在项目主页，点击右上角 **"+Create"**
2. 选择 **"VOLUME"**
3. Name：`uploads`
4. Mount Path：`/app/uploads`
5. 点击 "Add"
6. 重复步骤创建 `reports` Volume

#### 4.2 Volume 附加检查
确认 Volume 已正确附加到服务：

- [ ] `uploads` Volume 已附加到 Web 服务
- [ ] `reports` Volume 已附加到 Web 服务
- [ ] `reports` Volume 已附加到 Reminder-Cron 服务（如果需要）

**✅ Volume 检查完成**

---

## 🧪 部署后测试

### 测试 1：数据库连接测试

1. 进入 Web 服务
2. 点击 **"Shell"** 或 **"Terminal"**
3. 执行：
   ```bash
   cd backend && python3 init_db.py
   ```
4. **预期结果**：
   - ✅ 无错误输出
   - ✅ 显示 "✓ 6个表创建成功"
   - ✅ 显示 "✓ 数据库初始化完成"

**如果失败**：
- 检查 `DATABASE_URL` 变量是否正确
- 检查 Postgres 服务是否正常运行

---

### 测试 2：Web 服务健康检查

1. 获取 Web 服务的公共 URL
   - 在 Web 服务 → Networking → Public Networking
   - 点击 "Generate Domain" 或查看已有域名

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

**如果失败**：
- 检查端口配置（应该是 8000）
- 检查部署日志是否有错误
- 检查应用是否成功启动

---

### 测试 3：API 端点测试

访问根路径：
```bash
curl https://your-app.railway.app/
```

**预期结果**：
```json
{
  "name": "CreditPilot API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs"
}
```

访问 API 文档：
```
https://your-app.railway.app/docs
```

**预期结果**：
- ✅ 显示 Swagger UI 文档页面

---

### 测试 4：Cron 服务测试

1. 进入 Reminder-Cron 服务
2. 查看 **"Deployments"** 或 **"Logs"**
3. 等待到 UTC 14:00 或手动触发一次部署

**预期结果**：
- ✅ 服务在 Cron 时间启动
- ✅ 执行 `reminder_system.py`
- ✅ 生成 Excel 报告
- ✅ 发送邮件（检查收件箱）
- ✅ 日志中无错误

**如果失败**：
- 检查 Start Command 是否正确
- 检查 Cron Schedule 格式是否正确
- 检查所有环境变量是否设置
- 检查日志中的错误信息

---

## ⚠️ 常见问题排查

### 问题 1：DATABASE_URL 连接失败

**症状**：
- `init_db.py` 执行失败
- 显示数据库连接错误

**检查**：
1. 确认 `DATABASE_URL` 格式：`${{ Postgres.DATABASE_URL }}`
2. 确认 Postgres 服务名称正确（区分大小写）
3. 确认 Postgres 服务正在运行

**解决**：
- 重新设置 `DATABASE_URL` 变量
- 检查 Postgres 服务状态

---

### 问题 2：端口错误

**症状**：
- Web 服务无法访问
- 显示端口被占用或连接失败

**检查**：
1. Networking → Port 设置为 `8000`
2. 代码中使用 `os.getenv("PORT", 8000)`
3. 启动脚本使用 `${PORT:-8000}`

**解决**：
- 确认端口配置一致
- 重新部署服务

---

### 问题 3：Volume 路径错误

**症状**：
- 文件上传失败
- 报告生成失败
- 显示路径不存在

**检查**：
1. Volume Mount Path：`/app/uploads`, `/app/reports`
2. 代码中使用：`/app/uploads`, `/app/reports`
3. Volume 已正确附加到服务

**解决**：
- 确认路径一致
- 重新挂载 Volume

---

### 问题 4：Cron 不执行

**症状**：
- 定时任务不运行
- 邮件未发送

**检查**：
1. Cron Schedule 格式：`0 14 * * *`
2. Start Command：`cd backend && python3 reminder_system.py`
3. 所有环境变量已设置

**解决**：
- 检查 Cron Schedule 格式
- 检查 Start Command 是否正确
- 查看部署日志

---

### 问题 5：邮件发送失败

**症状**：
- Cron 执行但邮件未发送
- 显示 SMTP 错误

**检查**：
1. `SENDER_EMAIL` 是否正确
2. `SENDER_PASSWORD` 是否正确（Gmail 应用密码）
3. `SMTP_SERVER` = `smtp.gmail.com`
4. `SMTP_PORT` = `587`
5. `RECIPIENT_EMAIL` 是否正确

**解决**：
- 确认所有邮件相关变量
- 检查 Gmail 应用密码是否有效
- 查看日志中的错误信息

---

## 📊 配置验证总结

### 必需配置项

| 配置项 | Web 服务 | Reminder-Cron 服务 | Postgres 服务 |
|--------|----------|-------------------|---------------|
| DATABASE_URL | ✅ `${{ Postgres.DATABASE_URL }}` | ✅ `${{ Postgres.DATABASE_URL }}` | ✅ 自动生成 |
| 邮件变量 | ✅ 全部设置 | ✅ 全部设置 | ❌ 不需要 |
| 路径变量 | ✅ 全部设置 | ✅ 全部设置 | ❌ 不需要 |
| Volume | ✅ uploads, reports | ✅ reports | ❌ 不需要 |
| Port | ✅ 8000 | ❌ 不需要 | ❌ 不需要 |
| Cron Schedule | ❌ 留空 | ✅ `0 14 * * *` | ❌ 留空 |
| Start Command | ❌ 留空 | ✅ `cd backend && python3 reminder_system.py` | ❌ 留空 |

---

## ✅ 验证完成检查清单

完成所有检查后，确认：

- [ ] Postgres 服务配置正确
- [ ] Web 服务配置正确
- [ ] Reminder-Cron 服务配置正确（如果使用方案B）
- [ ] Volume 已创建并挂载
- [ ] 所有环境变量已设置
- [ ] 数据库连接测试通过
- [ ] Web 服务健康检查通过
- [ ] API 端点可访问
- [ ] Cron 服务测试通过（如果使用方案B）

---

## 🚀 下一步

如果所有检查都通过：

1. ✅ 系统已准备好运行
2. ✅ 可以开始使用 CreditPilot
3. ✅ 等待 Cron 任务自动执行（每天 UTC 14:00）

如果发现问题：

1. 记录具体问题
2. 参考"常见问题排查"部分
3. 修复问题后重新测试

---

**检查完成时间**：2025-12-10  
**检查工具**：本验证指南
