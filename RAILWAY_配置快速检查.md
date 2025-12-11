# Railway 配置快速检查清单

**快速版本** - 用于快速验证 Railway 配置

---

## ⚡ 5分钟快速检查

### 1. Postgres 服务（30秒）
- [ ] Variables 中有 `DATABASE_URL`（自动生成，不要修改）
- [ ] Settings 中 Start Command 和 Cron Schedule 都留空

### 2. Web 服务（2分钟）
- [ ] Build → Builder = `Dockerfile`
- [ ] Deploy → Start Command = **留空**
- [ ] Networking → Port = `8000`
- [ ] Variables → `DATABASE_URL` = `${{ Postgres.DATABASE_URL }}` ⚠️ **关键**
- [ ] Variables → 其他变量已设置（邮件、路径）
- [ ] Volumes → `uploads` 和 `reports` 已挂载

### 3. Reminder-Cron 服务（1分钟）
- [ ] Deploy → Start Command = `cd backend && python3 reminder_system.py`
- [ ] Deploy → Cron Schedule = `0 14 * * *`
- [ ] Variables → `DATABASE_URL` = `${{ Postgres.DATABASE_URL }}`
- [ ] Variables → 其他变量已设置

### 4. Volume（30秒）
- [ ] 已创建 `uploads` 和 `reports` Volume
- [ ] 已附加到相应服务

---

## 🧪 快速测试（1分钟）

### 测试 1：数据库连接
```bash
# 在 Web 服务 Shell 中执行
cd backend && python3 init_db.py
```
- [ ] 无错误，显示 "✓ 数据库初始化完成"

### 测试 2：Web 服务
```bash
# 访问健康检查
curl https://your-app.railway.app/health
```
- [ ] 返回 `{"status": "healthy"}`

---

## ⚠️ 关键检查点

1. **DATABASE_URL 格式**：`${{ Postgres.DATABASE_URL }}`（双大括号）
2. **端口**：`8000`
3. **路径**：`/app/uploads`, `/app/reports`
4. **Cron**：`0 14 * * *`（在 Reminder-Cron 服务中）

---

## ✅ 全部通过 = 系统可以运行！

如果所有检查项都打勾 ✅，系统应该可以顺利运行。

---

**详细检查**：查看 `RAILWAY_CONFIGURATION_VERIFICATION.md`
