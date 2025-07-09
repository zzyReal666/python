# 基于官方 Python 3.11 精简版镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt ./
COPY pyproject.toml ./

# 安装依赖
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 复制项目全部代码
COPY . .

# 暴露日志演示端口
EXPOSE 7862

# 启动日志演示应用（可根据需要修改为其它模块）
CMD ["python", "src/main.py", "run", "LoggingDemoApp"] 