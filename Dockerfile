# 使用官方的 Python 镜像作为基础镜像
FROM python:3.11

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到工作目录
COPY . /app

# 安装依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 23080

# 启动服务
CMD ["python", "main.py"]