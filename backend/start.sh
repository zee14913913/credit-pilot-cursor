#!/bin/bash
# Railway 启动脚本

echo "============================================================"
echo "CreditPilot 启动中..."
echo "============================================================"

# 初始化数据库
echo "初始化数据库..."
python3 init_db.py

# 启动服务器
echo "启动API服务器..."
python3 -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
