# 我的天文台应用自动化测试框架

## 📋 项目概述

这是一个基于 **Python + Behave + Appium** 的移动应用自动化测试框架，专门为"我的天文台"天气应用设计。该框架采用 BDD（行为驱动开发）模式，提供了完整的测试解决方案。

### 🎯 主要特性

- ✅ **BDD 测试模式**: 使用 Gherkin 语法编写测试用例，业务人员也能理解
- ✅ **跨平台支持**: 支持 Android 和 iOS 平台
- ✅ **页面对象模式**: 良好的代码结构和可维护性
- ✅ **数据驱动测试**: 结构化管理测试数据
- ✅ **详细报告**: 支持多种报告格式（HTML、Allure 等）
- ✅ **失败截图**: 自动保存失败场景的截图
- ✅ **并行执行**: 支持并行运行测试用例
- ✅ **环境配置**: 灵活的配置文件管理

## 🏗️ 项目结构

```
AppAutomationFramework/
├── features/                          # Behave测试文件
│   ├── steps/                         # 测试步骤实现
│   │   └── weather_app_steps.py       # 天气应用测试步骤
│   ├── environment.py                 # Behave环境配置
│   └── weather_app.feature            # 测试用例文件
├── config/                            # 配置文件
│   └── config.yaml                    # 应用配置
├── test_data/                         # 测试数据
│   └── weather_data.yaml              # 天气测试数据
├── utils/                             # 工具类
│   ├── app_driver.py                  # APP驱动管理
│   ├── test_data_manager.py           # 测试数据管理
│   └── page_objects.py                # 页面对象模型
├── reports/                           # 测试报告
├── screenshots/                       # 失败截图
├── requirements.txt                   # Python依赖
├── behave.ini                         # Behave配置
├── run_tests.py                       # 测试运行脚本
└── README.md                          # 项目文档
```

## 🚀 快速开始

### 1. 环境准备

#### 1.1 安装 Python

确保您的系统已安装 Python 3.7 或更高版本：

```bash
python --version
```

#### 1.2 安装 Node.js 和 Appium

```bash
# 安装Node.js (如果未安装)
# 下载地址: https://nodejs.org/

# 安装Appium
npm install -g appium

# 验证安装
appium --version
```

#### 1.3 安装 Android SDK (Android 测试)

- 下载并安装 Android Studio
- 配置 ANDROID_HOME 环境变量
- 创建 Android 模拟器或连接真机

#### 1.4 安装 Xcode (iOS 测试，仅 macOS)

- 从 App Store 安装 Xcode
- 安装 iOS 模拟器

### 2. 项目部署

#### 2.1 克隆项目

```bash
git clone <项目地址>
cd AppAutomationFramework
```

#### 2.2 安装 Python 依赖

```bash
pip install -r requirements.txt
```

#### 2.3 配置应用信息

编辑 `config/config.yaml` 文件，根据您的环境修改配置：

```yaml
# 修改应用包名和活动名
environments:
  android:
    app_package: "com.weather.forecast.weatherlive"
    app_activity: "com.weather.forecast.weatherlive.MainActivity"
```

#### 2.4 启动 Appium 服务器

```bash
# 启动Appium服务器
appium
```

### 3. 运行测试

#### 3.1 基本运行

```bash
# 运行所有测试
python run_tests.py

# 或直接使用behave
behave
```

#### 3.2 高级运行选项

```bash
# 运行冒烟测试
python run_tests.py --smoke

# 运行回归测试
python run_tests.py --regression

# 生成测试报告
python run_tests.py --report

# 生成Allure报告
python run_tests.py --allure

# 并行执行测试
python run_tests.py --parallel

# 按标签运行测试
python run_tests.py --tags "@smoke"
```

#### 3.3 使用 behave 命令

```bash
# 运行所有测试
behave

# 运行特定标签的测试
behave --tags="@smoke"

# 生成JSON报告
behave --format=json --outfile=reports/report.json

# 并行执行
behave --processes=2
```

## 📝 测试用例编写

### 1. 创建 Feature 文件

在 `features/` 目录下创建 `.feature` 文件：

```gherkin
# language: zh-CN
功能: 天气查询功能
  作为用户
  我希望能够查询不同城市的天气
  以便了解天气状况

  场景: 查询北京天气
    假设我打开了我的天文台应用
    当我搜索城市 "北京"
    并且我选择城市 "北京"
    那么我应该看到当前温度信息
    并且我应该看到天气描述
```

### 2. 实现测试步骤

在 `features/steps/` 目录下创建步骤实现文件：

```python
from behave import given, when, then
from utils.app_driver import AppDriver

@given('我打开了我的天文台应用')
def step_open_app(context):
    context.driver = AppDriver()
    context.driver.start_driver()

@when('我搜索城市 "{city_name}"')
def step_search_city(context, city_name):
    # 实现搜索逻辑
    pass
```

### 3. 添加测试数据

在 `test_data/` 目录下创建 YAML 文件：

```yaml
cities:
  beijing:
    name: "北京"
    coordinates:
      latitude: 39.9042
      longitude: 116.4074
```

## 🔧 配置说明

### 1. 应用配置 (config/config.yaml)

```yaml
# Appium服务器配置
appium:
  host: "127.0.0.1"
  port: 4723

# 测试环境配置
environments:
  android:
    platform_name: "Android"
    automation_name: "UiAutomator2"
    device_name: "Android Emulator"
    app_package: "com.weather.forecast.weatherlive"
    app_activity: "com.weather.forecast.weatherlive.MainActivity"
```

### 2. Behave 配置 (behave.ini)

```ini
[behave]
format=pretty
show_skipped=true
show_timings=true
verbose=true
```

## 📊 测试报告

### 1. 控制台报告

运行测试时会显示详细的执行信息：

```
==================================================
开始执行我的天文台应用自动化测试
开始时间: 2024-01-15 10:30:00
==================================================

开始执行特性: 我的天文台应用自动化测试
  - 开始执行场景: 查看不同城市的天气信息
    - 执行步骤: 我打开了我的天文台应用
    - 步骤通过: 我打开了我的天文台应用
```

### 2. HTML 报告

```bash
python run_tests.py --report
```

### 3. Allure 报告

```bash
# 生成Allure报告
python run_tests.py --allure

# 查看报告
allure serve reports/allure-results
```

## 🐛 故障排除

### 1. Appium 连接问题

```bash
# 检查Appium服务器状态
curl http://127.0.0.1:4723/status

# 重启Appium服务器
appium --reset
```

### 2. 设备连接问题

```bash
# 检查Android设备
adb devices

# 检查iOS设备
xcrun simctl list devices
```

### 3. 元素定位问题

- 使用 Appium Inspector 查看元素
- 检查元素 ID 是否正确
- 确认应用版本兼容性
  ### 4. 常见错误解决

#### 错误: "No such element"

- 检查元素定位器是否正确
- 增加等待时间
- 确认页面已完全加载

#### 错误: "Session not created"

- 检查设备连接状态
- 确认应用已安装
- 验证 Appium 配置

## 🔄 CI/CD 集成

### 1. GitHub Actions

创建 `.github/workflows/test.yml`：

```yaml
name: 自动化测试
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: 设置Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: 安装依赖
        run: pip install -r requirements.txt
      - name: 运行测试
        run: python run_tests.py --report
```

### 2. Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'python run_tests.py --report'
            }
        }
    }
}
```

## 📈 最佳实践

### 1. 测试用例设计

- 使用清晰的场景描述
- 保持测试用例独立性
- 合理使用背景和场景大纲

### 2. 代码组织

- 遵循页面对象模式
- 将测试数据与测试逻辑分离
- 使用有意义的变量名和函数名

### 3. 错误处理

- 添加适当的等待机制
- 实现失败重试机制
- 保存详细的错误信息

### 4. 性能优化

- 使用并行执行提高效率
- 优化元素定位策略
- 减少不必要的等待时间

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 项目 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 邮箱: your-email@example.com

---

**注意**: 使用前请确保已正确配置 Appium 环境和测试设备。
