# CreditPilot 快速开始指南

## 🎯 三个问题的答案

### 1️⃣ 我到哪里使用？

**当前可用方式：**

#### 方式A：浏览器（最简单，推荐）⭐
1. 启动服务器后
2. 打开浏览器访问：**http://localhost:8000/docs**
3. 在网页上直接测试所有功能

#### 方式B：命令行
- 使用 `curl` 命令
- 使用 `test_api.py` 脚本

#### 方式C：iPad App（开发中）
- 目前还在开发，完成后可以在iPad上使用

---

### 2️⃣ 怎么使用？

#### 第一步：启动服务器

```bash
# 1. 进入项目目录
cd /Users/1491-3913zee/Projects/CreditPilot/backend

# 2. 首次使用：安装依赖
pip install -r requirements.txt

# 3. 首次使用：初始化数据库
python3 database.py

# 4. 启动服务器
python3 main.py
```

**看到这个就成功了：**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 第二步：打开浏览器

访问：**http://localhost:8000/docs**

你会看到一个漂亮的API文档页面，可以直接：
- ✅ 上传PDF账单
- ✅ 查看所有账单
- ✅ 查看Dashboard统计
- ✅ 测试提醒系统

#### 第三步：上传PDF账单

1. 在API文档页面，找到 `POST /api/statements/upload`
2. 点击 "Try it out"
3. 点击 "Choose File" 选择你的PDF文件
4. 点击 "Execute"
5. 系统自动解析并显示结果！

---

### 3️⃣ 提醒是以什么形式提醒？

**当前已实现的提醒形式：**

#### 📺 形式1：控制台输出（终端显示）

运行提醒系统时，会在终端显示：

```
============================================================
📋 CreditPilot 明日到期提醒
============================================================

明天到期 (2025-01-28):
1️⃣ CHANG CHOON CHOW - Alliance Bank *4514
   💰 GZ Pay: RM 1,500.00 ✓ 已付
   💰 Owner Pay: RM 0.00 ⚠️ 待付款
   📎 单据: 3/3 ✓

------------------------------------------------------------
总计需代付 (GZ): RM 2,300.00
总计需客户付 (Owner): RM 700.00
合计: RM 3,000.00

🔴 最紧急: CHOW KAH FEI (RM 1,500.00)
   原因: GZ需代付 RM 800.00 | Owner需付款 RM 700.00 | 缺少2份单据
============================================================
```

**如何查看：**
```bash
cd backend
python3 reminder_system.py
```

#### 📊 形式2：Excel日报文件

系统自动生成Excel文件，保存在：
```
/Users/1491-3913zee/Projects/CreditPilot/reports/
CreditPilot_Daily_Report_20250128.xlsx
```

Excel包含：
- 明天到期的账单列表
- 后天到期的账单列表
- 总计金额
- 最紧急客户

**如何获取：**
- 自动生成（运行提醒系统时）
- 或通过API下载：`http://localhost:8000/api/reminders/daily-report`

#### 🔌 形式3：API JSON数据

通过API获取提醒数据（JSON格式）：

```bash
curl http://localhost:8000/api/reminders/test
```

返回JSON数据，可以在程序中处理。

---

### ⏰ 定时提醒（每晚10点）

#### 立即测试（不等到晚上10点）：
```bash
cd backend
python3 reminder_system.py
```

#### 启动定时调度器（后台运行）：
```bash
cd backend
python3 -c "from reminder_system import setup_scheduler; setup_scheduler()"
```

---

### 📱 未来提醒形式（iPad App开发完成后）

1. **iPad本地通知** 🔔
   - 每晚10点自动弹出通知
   - 显示提醒摘要
   - 点击打开App查看详情

2. **App内提醒** 📱
   - Dashboard显示红色角标
   - 专门的提醒页面

---

## 🚀 完整使用流程示例

### 场景：上传一张新账单

```bash
# 1. 启动服务器（保持运行）
cd /Users/1491-3913zee/Projects/CreditPilot/backend
python3 main.py
```

**在浏览器中：**
1. 打开 `http://localhost:8000/docs`
2. 找到 `POST /api/statements/upload`
3. 上传PDF文件
4. 查看解析结果

**或使用命令行：**
```bash
curl -X POST "http://localhost:8000/api/statements/upload" \
  -F "file=@/path/to/your/statement.pdf"
```

### 场景：查看明日到期提醒

**方法1：浏览器**
- 访问 `http://localhost:8000/api/dashboard/upcoming`

**方法2：命令行**
```bash
curl http://localhost:8000/api/dashboard/upcoming
```

**方法3：运行提醒系统**
```bash
cd backend
python3 reminder_system.py
```

---

## 📋 总结

| 问题 | 答案 |
|------|------|
| **到哪里使用？** | 浏览器访问 `http://localhost:8000/docs`（最简单） |
| **怎么使用？** | 1) 启动服务器 2) 打开浏览器 3) 在API文档页面上传PDF |
| **提醒形式？** | 1) 控制台输出 2) Excel文件 3) API JSON（未来：iPad通知） |

---

## 💡 推荐使用方式

**日常使用：**
1. 启动服务器：`python3 main.py`
2. 打开浏览器：`http://localhost:8000/docs`
3. 在网页上直接操作，无需命令行

**查看提醒：**
- 浏览器访问：`http://localhost:8000/api/dashboard/upcoming`
- 或运行：`python3 reminder_system.py` 查看详细提醒

---

需要更多帮助？查看 `USAGE_GUIDE.md` 获取详细说明。
