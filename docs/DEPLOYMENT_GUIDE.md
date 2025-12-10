# CreditPilot 完整部署指南

## 📋 目录
1. [系统要求](#系统要求)
2. [后端部署](#后端部署)
3. [定时提醒配置](#定时提醒配置)
4. [iPad App开发](#ipad-app开发)
5. [常见问题](#常见问题)

---

## 系统要求

### 硬件要求
- **服务器:** 
  - CPU: 2核心以上
  - 内存: 4GB以上
  - 硬盘: 50GB以上（存储PDF和单据）
  
- **iPad:**
  - iPad Air或Pro（推荐）
  - iOS 15+
  - 支持Apple Pencil（可选）

### 软件要求
- Python 3.10+
- PostgreSQL 13+ 或 SQLite 3
- Tesseract OCR
- Xcode 14+（开发iPad App）

---

## 后端部署

### 步骤1：安装依赖

```bash
# 进入项目目录
cd /home/claude/CreditPilot/backend

# 安装Python依赖
pip install -r requirements.txt --break-system-packages
```

**requirements.txt 内容：**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-multipart==0.0.6
pdfplumber==0.10.3
pytesseract==0.3.10
Pillow==10.1.0
pandas==2.1.3
openpyxl==3.1.2
apscheduler==3.10.4
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

### 步骤2：配置环境变量

创建 `.env` 文件：

```bash
# 数据库配置
DATABASE_URL=sqlite:///./creditpilot.db
# 生产环境使用PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/creditpilot

# API配置
API_HOST=0.0.0.0
API_PORT=8000

# 文件存储
UPLOAD_DIR=/home/claude/CreditPilot/uploads
REPORTS_DIR=/home/claude/CreditPilot/reports

# 提醒配置
REMINDER_TIME=22:00
REMINDER_ENABLED=true
```

### 步骤3：初始化数据库

```bash
cd /home/claude/CreditPilot/backend
python3 database.py
```

输出：
```
✓ 6个表创建成功
✓ 数据库初始化完成
```

### 步骤4：启动API服务器

#### 开发模式（调试）
```bash
cd /home/claude/CreditPilot/backend
python3 main.py
```

#### 生产模式（后台运行）
```bash
cd /home/claude/CreditPilot/backend
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &
```

#### 使用systemd服务（推荐）

1. 创建服务文件：
```bash
sudo cp /home/claude/CreditPilot/deployment/creditpilot-api.service /etc/systemd/system/
```

2. 启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl start creditpilot-api
sudo systemctl enable creditpilot-api
```

3. 检查状态：
```bash
sudo systemctl status creditpilot-api
```

### 步骤5：测试API

```bash
cd /home/claude/CreditPilot/backend
python3 test_api.py
```

预期输出：
```
✓ GET / - 200 OK
✓ GET /api/dashboard/stats - 200 OK
✓ GET /api/dashboard/upcoming - 200 OK
✓ GET /api/statements - 200 OK
✓ 所有测试完成
```

### 步骤6：访问API文档

浏览器打开：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 定时提醒配置

### 方法1：使用内置调度器（推荐）

#### 启动定时提醒服务

```bash
cd /home/claude/CreditPilot/backend
python3 -c "from reminder_system import setup_scheduler; setup_scheduler()"
```

输出：
```
============================================================
CreditPilot 定时提醒系统已启动
每晚22:00执行提醒任务
============================================================
```

#### 作为systemd服务运行（后台）

1. 复制服务文件：
```bash
sudo cp /home/claude/CreditPilot/deployment/creditpilot-reminder.service /etc/systemd/system/
```

2. 启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl start creditpilot-reminder
sudo systemctl enable creditpilot-reminder
```

3. 查看日志：
```bash
sudo journalctl -u creditpilot-reminder -f
```

### 方法2：使用cron（备选）

编辑crontab：
```bash
crontab -e
```

添加：
```
# 每晚10点执行提醒
0 22 * * * cd /home/claude/CreditPilot/backend && /usr/bin/python3 reminder_system.py >> /home/claude/CreditPilot/logs/reminder.log 2>&1
```

### 测试提醒系统

立即执行一次（不等到晚上10点）：
```bash
cd /home/claude/CreditPilot/backend
python3 reminder_system.py
```

或通过API：
```bash
curl http://localhost:8000/api/reminders/test
```

### 查看Excel日报

日报保存在：
```
/home/claude/CreditPilot/reports/CreditPilot_Daily_Report_YYYYMMDD.xlsx
```

或通过API下载：
```bash
curl -O http://localhost:8000/api/reminders/daily-report
```

---

## iPad App开发

### 架构概览

```
CreditPilot.app (SwiftUI)
├── Views/
│   ├── DashboardView.swift
│   ├── StatementDetailView.swift
│   ├── UploadView.swift
│   └── ReminderView.swift
├── Models/
│   ├── Statement.swift
│   └── Client.swift
├── Services/
│   ├── APIClient.swift
│   ├── PDFService.swift
│   └── NotificationService.swift
└── Resources/
```

### 快速开始

#### 1. 创建Xcode项目

```bash
# 打开Xcode
# File > New > Project
# 选择: iOS > App
# Interface: SwiftUI
# Language: Swift
# Product Name: CreditPilot
```

#### 2. 配置API客户端

**APIClient.swift:**
```swift
import Foundation

class APIClient {
    static let shared = APIClient()
    let baseURL = "http://YOUR_SERVER_IP:8000"
    
    func fetchUpcoming() async throws -> UpcomingResponse {
        let url = URL(string: "\(baseURL)/api/dashboard/upcoming")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(UpcomingResponse.self, from: data)
    }
    
    func uploadPDF(_ fileURL: URL) async throws -> UploadResponse {
        var request = URLRequest(url: URL(string: "\(baseURL)/api/statements/upload")!)
        request.httpMethod = "POST"
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n")
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(fileURL.lastPathComponent)\"\r\n")
        body.append("Content-Type: application/pdf\r\n\r\n")
        body.append(try Data(contentsOf: fileURL))
        body.append("\r\n--\(boundary)--\r\n")
        
        request.httpBody = body
        
        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(UploadResponse.self, from: data)
    }
}
```

#### 3. 配置本地通知

**NotificationService.swift:**
```swift
import UserNotifications

class NotificationService {
    static let shared = NotificationService()
    
    func requestPermission() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            if granted {
                print("✓ 通知权限已授予")
            }
        }
    }
    
    func scheduleDaily10PMReminder() {
        let content = UNMutableNotificationContent()
        content.title = "CreditPilot提醒"
        content.body = "请查看明日到期账单"
        content.sound = .default
        
        var dateComponents = DateComponents()
        dateComponents.hour = 22
        dateComponents.minute = 0
        
        let trigger = UNCalendarNotificationTrigger(dateMatching: dateComponents, repeats: true)
        let request = UNNotificationRequest(identifier: "daily-reminder", content: content, trigger: trigger)
        
        UNUserNotificationCenter.current().add(request)
    }
}
```

#### 4. Dashboard示例

**DashboardView.swift:**
```swift
import SwiftUI

struct DashboardView: View {
    @State private var upcoming: UpcomingResponse?
    @State private var isLoading = true
    
    var body: some View {
        NavigationView {
            VStack {
                if isLoading {
                    ProgressView("加载中...")
                } else if let data = upcoming {
                    List {
                        Section("未来2天到期") {
                            HStack {
                                Text("明天到期")
                                Spacer()
                                Text("\(data.tomorrowCount) 笔")
                                    .foregroundColor(.orange)
                            }
                            HStack {
                                Text("后天到期")
                                Spacer()
                                Text("\(data.dayAfterCount) 笔")
                                    .foregroundColor(.blue)
                            }
                        }
                        
                        Section("待付款") {
                            HStack {
                                Text("GZ代付")
                                Spacer()
                                Text("RM \(data.totalGzPayment, specifier: "%.2f")")
                                    .foregroundColor(.red)
                            }
                            HStack {
                                Text("Owner付款")
                                Spacer()
                                Text("RM \(data.totalOwnerPayment, specifier: "%.2f")")
                                    .foregroundColor(.green)
                            }
                        }
                        
                        if let urgent = data.mostUrgentClient {
                            Section("最紧急") {
                                Text(urgent)
                                    .foregroundColor(.red)
                                    .bold()
                            }
                        }
                    }
                }
            }
            .navigationTitle("CreditPilot")
            .task {
                await loadData()
            }
        }
    }
    
    func loadData() async {
        do {
            upcoming = try await APIClient.shared.fetchUpcoming()
            isLoading = false
        } catch {
            print("加载失败: \(error)")
        }
    }
}
```

---

## 常见问题

### Q1: API连接失败

**检查清单：**
1. API服务器是否正在运行？
   ```bash
   curl http://localhost:8000/
   ```

2. 防火墙是否开放8000端口？
   ```bash
   sudo ufw allow 8000
   ```

3. iPad和服务器在同一网络吗？
   - 同一WiFi网络
   - 或使用公网IP

### Q2: 提醒没有在晚上10点触发

**检查清单：**
1. 提醒服务是否正在运行？
   ```bash
   sudo systemctl status creditpilot-reminder
   ```

2. 查看日志：
   ```bash
   sudo journalctl -u creditpilot-reminder -f
   ```

3. 时区是否正确？
   ```bash
   date
   timedatectl
   ```

### Q3: PDF解析失败

**可能原因：**
1. PDF格式不匹配（目前只支持Alliance Bank）
2. PDF加密或损坏

**解决方案：**
- 检查PDF文件是否正常打开
- 确认是Alliance Bank账单
- 查看API错误日志

### Q4: Excel日报没有生成

**检查：**
```bash
ls -lh /home/claude/CreditPilot/reports/
```

**手动生成：**
```bash
cd /home/claude/CreditPilot/backend
python3 reminder_system.py
```

---

## 生产部署建议

### 1. 使用HTTPS
```bash
# 安装certbot
sudo apt install certbot

# 获取SSL证书
sudo certbot certonly --standalone -d yourdomain.com
```

### 2. 使用Nginx反向代理

**/etc/nginx/sites-available/creditpilot:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. 数据备份

每日自动备份：
```bash
# 添加到crontab
0 2 * * * pg_dump creditpilot > /backups/creditpilot_$(date +\%Y\%m\%d).sql
```

### 4. 监控和日志

使用PM2管理进程：
```bash
pip install pm2
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name creditpilot-api
pm2 logs creditpilot-api
```

---

## 支持和帮助

### 日志位置
- API日志: `/home/claude/CreditPilot/logs/api.log`
- 提醒日志: `/home/claude/CreditPilot/logs/reminder.log`
- 系统日志: `sudo journalctl -u creditpilot-*`

### 检查系统状态
```bash
# API服务
sudo systemctl status creditpilot-api

# 提醒服务
sudo systemctl status creditpilot-reminder

# 数据库
psql -U postgres -d creditpilot -c "SELECT COUNT(*) FROM statements;"
```

---

**部署完成！现在系统应该：**
✅ API服务器运行在 http://localhost:8000  
✅ 每晚10点自动发送提醒  
✅ 自动生成Excel日报  
✅ 准备好连接iPad App
