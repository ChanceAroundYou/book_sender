FROM python:3.12-slim

# 使用 sed 将 apt 源切换为清华源（兼容 deb822 与传统 sources.list），并校验后再安装
RUN set -eux; \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
    sed -ri \
    -e 's@URIs:[[:space:]]*https?://deb\.debian\.org/debian@URIs: https://mirrors.tuna.tsinghua.edu.cn/debian@g' \
    -e 's@URIs:[[:space:]]*https?://security\.debian\.org/debian-security@URIs: https://mirrors.tuna.tsinghua.edu.cn/debian-security@g' \
    -e 's@URIs:[[:space:]]*https?://deb\.debian\.org/debian-security@URIs: https://mirrors.tuna.tsinghua.edu.cn/debian-security@g' \
    /etc/apt/sources.list.d/debian.sources; \
    fi; \
    apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 继续在同一阶段：安装运行时依赖（包含之前两个阶段的合集）
RUN set -eux; \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
    sed -ri \
    -e 's@URIs:[[:space:]]*https?://deb\.debian\.org/debian@URIs: https://mirrors.tuna.tsinghua.edu.cn/debian@g' \
    -e 's@URIs:[[:space:]]*https?://security\.debian\.org/debian-security@URIs: https://mirrors.tuna.tsinghua.edu.cn/debian-security@g' \
    -e 's@URIs:[[:space:]]*https?://deb\.debian\.org/debian-security@URIs: https://mirrors.tuna.tsinghua.edu.cn/debian-security@g' \
    /etc/apt/sources.list.d/debian.sources; \
    fi; \
    apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libgl1 \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 加速 Playwright 浏览器下载（国内镜像）并安装 chromium
ENV PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright
RUN playwright install chromium

# 复制应用代码
COPY app/ app/

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]