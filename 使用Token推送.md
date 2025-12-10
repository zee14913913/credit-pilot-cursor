# 🔐 使用 Token 推送代码

## ✅ 你已经拿到 Token 了！

现在只需要执行推送命令，然后在提示时输入token。

---

## 📋 推送步骤

### 第一步：打开终端（Terminal）

1. **打开 "终端" 应用**
   - 在 Mac 上，按 `Command + 空格`，输入 "终端" 或 "Terminal"
   - 或者打开 "应用程序" → "实用工具" → "终端"

### 第二步：进入项目目录

**在终端中输入：**

```bash
cd /Users/1491-3913zee/Projects/CreditPilot
```

**按回车**

### 第三步：执行推送命令

**在终端中输入：**

```bash
git push -u origin main
```

**按回车**

### 第四步：输入认证信息

**系统会提示你输入：**

1. **Username for 'https://github.com':**
   - 输入：`1491-3913zee`
   - 按回车

2. **Password for 'https://1491-3913zee@github.com':**
   - ⚠️ **重要：** 这里输入的是你刚才复制的 **token**，不是你的GitHub密码
   - 粘贴你刚才复制的token（类似：`ghp_xxxxxxxxxxxxxxxxxxxx`）
   - 按回车

**注意：** 输入密码时，终端不会显示任何字符（这是正常的，为了安全）

### 第五步：等待推送完成

**如果成功，你会看到：**

```
Enumerating objects: 67, done.
Counting objects: 100% (67/67), done.
Delta compression using up to 8 threads
Compressing objects: 100% (55/55), done.
Writing objects: 100% (67/67), 123.45 KiB | 1.23 MiB/s, done.
To https://github.com/1491-3913zee/credit-pilot-cursor.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**看到这个就成功了！** ✅

---

## 🎯 完整命令（复制粘贴）

**你可以直接复制这些命令到终端：**

```bash
cd /Users/1491-3913zee/Projects/CreditPilot
git push -u origin main
```

**然后按照提示输入：**
- Username: `1491-3913zee`
- Password: 粘贴你的token

---

## ✅ 推送成功后

1. **访问 GitHub 查看代码：**
   - https://github.com/1491-3913zee/credit-pilot-cursor
   - 应该能看到所有文件

2. **然后在 Railway 部署：**
   - 访问：https://railway.app
   - 用 GitHub 登录
   - 点击 "New Project" → "Deploy from GitHub repo"
   - 选择 `credit-pilot-cursor` 仓库

---

## 🆘 如果遇到问题

### 问题1：提示 "Authentication failed"

**解决：**
- 确认输入的是 token，不是密码
- 确认 token 没有过期
- 重新复制 token（确保没有多余空格）

### 问题2：提示 "Repository not found"

**解决：**
- 确认仓库名是否正确：`credit-pilot-cursor`
- 确认仓库是否存在
- 确认你有权限访问该仓库

---

## 💡 提示

- **Token 只输入一次**：Mac 的 Keychain 会记住，下次不需要再输入
- **输入密码时不显示**：这是正常的，为了安全
- **Token 要保密**：不要分享给任何人

---

**按照上面的步骤操作，就能完成推送了！** 🚀
