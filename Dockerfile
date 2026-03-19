# 使用轻量级 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖 (xxd 和 netcat 用于 wol.sh)
RUN apt-get update && apt-get install -y \
    vim \
    netcat-openbsd \
    xxd \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 给脚本添加执行权限
RUN chmod +x scripts/wol.sh

# 暴露端口
EXPOSE 8000

# 运行应用
CMD ["python", "main.py"]
