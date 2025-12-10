FROM python:3.11-slim

WORKDIR /app

# 基本环境配置
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 安装构建依赖与图像处理所需的系统库（Pillow 等）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libjpeg-dev \
        zlib1g-dev \
        libpng-dev \
        libtiff5-dev \
        tk-dev \
        ghostscript && \
    rm -rf /var/lib/apt/lists/*

# 仅拷贝并安装后端依赖
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# 拷贝全部代码
COPY . .

# 确保启动脚本可执行
RUN chmod +x backend/start.sh

WORKDIR /app/backend

# 入口：使用已有的 start.sh（包含初始化数据库与启动 uvicorn）
CMD ["bash", "start.sh"]
