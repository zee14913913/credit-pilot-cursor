# CreditPilot 服务器状态

## ✅ 服务器已成功启动！

### 访问地址

- **API文档（Swagger UI）**: http://localhost:8000/docs
- **API根路径**: http://localhost:8000/
- **Dashboard统计**: http://localhost:8000/api/dashboard/stats
- **未来2天到期**: http://localhost:8000/api/dashboard/upcoming

### 服务器信息

- **状态**: ✅ 运行中
- **端口**: 8000
- **虚拟环境**: `/Users/1491-3913zee/Projects/CreditPilot/backend/venv`
- **数据库**: SQLite (`creditpilot.db`)

### 如何使用

1. **打开浏览器访问API文档**
   ```
   http://localhost:8000/docs
   ```

2. **在API文档页面可以：**
   - ✅ 查看所有API端点
   - ✅ 测试API功能
   - ✅ 上传PDF账单
   - ✅ 查看账单列表
   - ✅ 测试提醒系统

3. **上传PDF账单**
   - 在API文档页面找到 `POST /api/statements/upload`
   - 点击 "Try it out"
   - 选择PDF文件
   - 点击 "Execute"

### 测试命令

```bash
# 测试API是否运行
curl http://localhost:8000/

# 查看Dashboard统计
curl http://localhost:8000/api/dashboard/stats

# 查看未来2天到期账单
curl http://localhost:8000/api/dashboard/upcoming

# 测试提醒系统
curl http://localhost:8000/api/reminders/test
```

### 停止服务器

如果需要停止服务器：
```bash
pkill -f "python3 main.py"
```

### 重新启动服务器

```bash
cd /Users/1491-3913zee/Projects/CreditPilot/backend
source venv/bin/activate
python3 main.py
```

---

**服务器启动时间**: 2025-01-27  
**状态**: ✅ 运行正常
