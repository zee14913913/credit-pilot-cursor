#!/bin/bash
# CreditPilot Railway 快速部署脚本

echo "============================================================"
echo "CreditPilot Railway 部署脚本"
echo "============================================================"
echo ""

# 检查是否在正确的目录
if [ ! -f "railway.json" ]; then
    echo "❌ 错误：请在 CreditPilot 项目根目录运行此脚本"
    exit 1
fi

# 检查Git是否已初始化
if [ ! -d ".git" ]; then
    echo "初始化Git仓库..."
    git init
fi

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "添加所有文件..."
    git add .
    
    echo "提交更改..."
    git commit -m "CreditPilot system ready for Railway deployment"
else
    echo "✓ 所有文件已提交"
fi

echo ""
echo "============================================================"
echo "✅ 本地准备完成！"
echo "============================================================"
echo ""
echo "下一步："
echo ""
echo "1. 在 GitHub 创建仓库："
echo "   - 访问：https://github.com/new"
echo "   - 仓库名：CreditPilot"
echo "   - 不要勾选任何初始化选项"
echo ""
echo "2. 推送代码到 GitHub："
echo "   git remote add origin https://github.com/你的用户名/CreditPilot.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 在 Railway 部署："
echo "   - 访问：https://railway.app"
echo "   - 用 GitHub 登录"
echo "   - 点击 'New Project' → 'Deploy from GitHub repo'"
echo "   - 选择 CreditPilot 仓库"
echo ""
echo "4. 配置环境变量和数据库（详见：部署完成步骤.md）"
echo ""
echo "============================================================"
