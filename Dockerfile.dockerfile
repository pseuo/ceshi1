FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制必要的文件
COPY requirements.txt .
COPY main.py .
COPY GeoLite2-City.mmdb .
COPY GeoLite2-ASN.mmdb .
COPY GeoCN.mmdb .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 7887

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7887", "--no-server-header", "--proxy-headers"]
