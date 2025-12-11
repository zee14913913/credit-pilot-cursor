# Railway 配置检查清单（最终版）

**完全符合 Railway 官方文档**  
**使用前**：请按照 `RAILWAY_最终配置指南_官方标准.md` 完成配置

---

## ✅ 快速检查（5分钟）

### Postgres 服务
- [ ] Variables → `DATABASE_URL` 存在（自动生成，未修改）
- [ ] Settings → Start Command = **留空**
- [ ] Settings → Cron Schedule = **留空**

### Web 服务
- [ ] Build → Builder = `Dockerfile`
- [ ] Deploy → Start Command = **留空**
- [ ] Deploy → Cron Schedule = **留空**
- [ ] Networking → Port = `8000`
- [ ] Variables → `DATABASE_URL` = `${{ Postgres.DATABASE_URL }}` ⚠️ **关键**
- [ ] Variables → 所有其他变量已设置（8个变量）
- [ ] Volumes → `uploads` 和 `reports` 已挂载

### Reminder-Cron 服务（方案B）
- [ ] Deploy → Start Command = `cd backend && python3 reminder_system.py`
- [ ] Deploy → Cron Schedule = `0 14 * * *`
- [ ] Variables → `DATABASE_URL` = `${{ Postgres.DATABASE_URL }}`
- [ ] Variables → 所有其他变量已设置

### Volume（项目级别）
- [ ] `uploads` Volume 已创建
- [ ] `reports` Volume 已创建
- [ ] 已附加到相应服务

---

## 🧪 验证测试

### 测试 1：数据库连接
```bash
# 在 Web 服务 Shell 中执行
cd backend && python3 init_db.py
```
- [ ] 无错误
- [ ] 显示 "✅ 数据库初始化完成"

### 测试 2：Web 服务
```bash
curl https://your-app.railway.app/health
```
- [ ] 返回 `{"status": "healthy"}`

### 测试 3：Cron 服务
- [ ] 查看 Reminder-Cron 服务日志
- [ ] 在 UTC 14:00 执行
- [ ] 无错误

---

## ⚠️ 关键检查点

1. **DATABASE_URL 格式**：`${{ Postgres.DATABASE_URL }}`（双大括号）
2. **Cron 位置**：服务的 Settings → Deploy → Cron Schedule
3. **Volume 位置**：项目级别创建
4. **端口**：`8000`

---

## ✅ 全部通过 = 系统可以运行！

**检查完成时间**：_____________  
**检查人**：_____________
