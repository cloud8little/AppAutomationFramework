# 使用官方Python镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    curl \
    wget \
    unzip \
    nodejs \
    npm \
    git \
    && rm -rf /var/lib/apt/lists/*

# 设置Android SDK环境变量
ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/bin:$ANDROID_HOME/platform-tools

# 下载并安装Android SDK
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip \
    && unzip commandlinetools-linux-8512546_latest.zip -d /opt/android-sdk \
    && rm commandlinetools-linux-8512546_latest.zip

# 安装Android SDK组件
RUN yes | /opt/android-sdk/cmdline-tools/bin/sdkmanager --licenses || true \
    && /opt/android-sdk/cmdline-tools/bin/sdkmanager \
        "platform-tools" \
        "platforms;android-29" \
        "build-tools;29.0.3" \
        "system-images;android-29;google_apis;x86_64"

# 安装Appium
RUN npm install -g appium@latest \
    && npm install -g appium-doctor

# 复制项目文件
COPY requirements.txt .
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建必要的目录
RUN mkdir -p reports screenshots

# 暴露Appium端口
EXPOSE 4723

# 设置启动脚本
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 启动命令
ENTRYPOINT ["docker-entrypoint.sh"] 