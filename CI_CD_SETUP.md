# CI/CD 设置指南

本文档介绍如何设置和配置自动化测试的 CI/CD 流程。

## 📋 目录

- [GitHub Actions 配置](#github-actions-配置)
- [Docker 环境](#docker-环境)
- [本地开发](#本地开发)
- [故障排除](#故障排除)

## 🚀 GitHub Actions 配置

### 1. 自动触发

CI/CD 流程会在以下情况下自动触发：

- 推送到 `main` 或 `develop` 分支
- 创建 Pull Request 到 `main` 分支
- 手动触发（workflow_dispatch）

### 2. 工作流程

#### 主要测试流程 (`appium-test.yml`)

1. **环境设置**

   - Python 3.9
   - Node.js 18
   - Java 11
   - Android SDK

2. **Appium 安装**

   ```bash
   npm install -g appium@latest
   npm install -g appium-doctor
   ```

3. **测试执行**

   ```bash
   python run_tests.py --report
   ```

4. **结果上传**
   - 测试报告
   - 截图
   - Appium 日志

### 3. 配置步骤

1. 在 GitHub 仓库中创建 `.github/workflows/` 目录
2. 复制 `appium-test.yml` 到该目录
3. 提交并推送更改

## 🐳 Docker 环境

### 1. 构建镜像

```bash
docker build -t appium-test-framework .
```

### 2. 运行容器

```bash
# 使用docker-compose（推荐）
docker-compose up --build

# 或直接使用docker
docker run -p 4723:4723 -v $(pwd)/reports:/app/reports appium-test-framework
```

### 3. 环境变量

| 变量名           | 默认值           | 说明               |
| ---------------- | ---------------- | ------------------ |
| APPIUM_HOST      | 127.0.0.1        | Appium 服务器地址  |
| APPIUM_PORT      | 4723             | Appium 服务器端口  |
| ANDROID_HOME     | /opt/android-sdk | Android SDK 路径   |
| ANDROID_SDK_ROOT | /opt/android-sdk | Android SDK 根路径 |

## 💻 本地开发

### 1. 环境要求

- Python 3.8+
- Node.js 16+
- Java 11+
- Android SDK

### 2. 安装步骤

```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 安装Appium
npm install -g appium@latest
npm install -g appium-doctor

# 3. 验证安装
appium --version
appium-doctor --android
```

### 3. 运行测试

```bash
# 启动Appium服务器
appium &

# 运行测试
python run_tests.py --report
```

## 🔧 故障排除

### 1. Appium 连接问题

**问题**: 无法连接到 Appium 服务器
**解决方案**:

```bash
# 检查Appium状态
curl http://127.0.0.1:4723/status

# 重启Appium
pkill -f appium
appium --reset
```

### 2. Android SDK 问题

**问题**: Android SDK 未找到
**解决方案**:

```bash
# 设置环境变量
export ANDROID_HOME=/path/to/android-sdk
export ANDROID_SDK_ROOT=/path/to/android-sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools

# 验证安装
adb version
```

### 3. 权限问题

**问题**: Docker 容器权限不足
**解决方案**:

```bash
# 使用特权模式运行
docker run --privileged -p 4723:4723 appium-test-framework
```

### 4. 网络问题

**问题**: 无法下载依赖
**解决方案**:

```bash
# 使用国内镜像
npm config set registry https://registry.npmmirror.com
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 📊 监控和报告

### 1. 测试报告

- **HTML 报告**: `reports/test_report.html`
- **Allure 报告**: `reports/allure-results/`
- **截图**: `screenshots/`

### 2. 日志文件

- **Appium 日志**: `appium.log`
- **测试日志**: `reports/test.log`

### 3. 性能指标

- 测试执行时间
- 成功率
- 失败原因分析

## 🔄 持续集成最佳实践

### 1. 并行执行

使用矩阵策略并行测试多个 Python 版本：

```yaml
strategy:
  matrix:
    python-version: [3.8, 3.9, "3.10"]
```

### 2. 缓存优化

缓存依赖以加速构建：

```yaml
- name: 缓存Python依赖
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### 3. 条件执行

只在特定条件下运行测试：

```yaml
- name: 运行测试
  if: github.event_name == 'push' || github.event_name == 'pull_request'
  run: python run_tests.py
```

## 📞 支持

如有问题，请：

1. 查看 GitHub Actions 日志
2. 检查本地环境配置
3. 提交 Issue 到项目仓库

---

**注意**: 确保在 CI/CD 环境中正确配置了所有必要的环境变量和依赖。
