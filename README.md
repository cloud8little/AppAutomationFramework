# Simple Mobile App Automation Test Framework

## 📋 Project Overview

This is a mobile application automation testing framework based on **Python + Behave + Appium**, specifically designed for the "My Observatory" weather app. The framework adopts the BDD (Behavior-Driven Development) model and provides a complete testing solution.

### 🎯 Key Features

- ✅ **BDD Testing Model**: Test cases are written in Gherkin syntax, which is understandable even for business personnel.
- ✅ **Cross-Platform Support**: Supports both Android and iOS platforms.
- ✅ **Page Object Model**: Good code structure and maintainability.
- ✅ **Data-Driven Testing**: Structured management of test data.
- ✅ **Detailed Reports**: Supports multiple report formats (HTML, Allure, etc.).
- ✅ **Failure Screenshots**: Automatically saves screenshots of failed scenarios.
- ✅ **Parallel Execution**: Supports running test cases in parallel.
- ✅ **Environment Configuration**: Flexible configuration file management.

## 🏗️ Project Structure

```
AppAutomationFramework/
├── features/                          # Behave test files
│   ├── steps/                         # Test step implementations
│   │   └── weather_app_steps.py       # Weather app test steps
│   ├── environment.py                 # Behave environment configuration
│   └── weather_app.feature            # Test case file
├── config/                            # Configuration files
│   └── config.yaml                    # Application configuration
├── test_data/                         # Test data
│   └── weather_data.yaml              # Weather test data
├── utils/                             # Utility classes
│   ├── app_driver.py                  # App driver management
│   ├── test_data_manager.py           # Test data management
│   └── page_objects.py                # Page Object Model
├── reports/                           # Test reports
├── screenshots/                       # Failure screenshots
├── requirements.txt                   # Python dependencies
├── behave.ini                         # Behave configuration
├── run_tests.py                       # Test runner script
└── README.md                          # Project documentation
```

## 🚀 Quick Start

### 1. Environment Setup

#### 1.1 Install Python

Ensure that your system has Python 3.7 or higher installed:

```bash
python --version
```

#### 1.2 Install Node.js and Appium

```bash
# Install Node.js (if not already installed)
# Download from: https://nodejs.org/

# Install Appium
npm install -g appium

# Verify installation
appium --version
```

#### 1.3 Install Android SDK (for Android testing)

- Download and install Android Studio.
- Configure the ANDROID_HOME environment variable.
- Create an Android emulator or connect a real device.

#### 1.4 Install Xcode (for iOS testing, macOS only)

- Install Xcode from the App Store.
- Install the iOS simulator.

### 2. Project Deployment

#### 2.1 Clone the Project

```bash
git clone https://github.com/cloud8little/AppAutomationFramework.git
cd AppAutomationFramework
```

#### 2.2 Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 2.3 Configure Application Information

Edit the `config/config.yaml` file and modify the configuration according to your environment:

```yaml
# Modify the app package and activity names
environments:
  android:
    app_package: "com.weather.forecast.weatherlive"
    app_activity: "com.weather.forecast.weatherlive.MainActivity"
```

#### 2.4 Start the Appium Server

```bash
# Start the Appium server
appium
```

### 3. Running Tests

#### 3.1 Basic Run

```bash
# Run all tests
python run_tests.py

# Or use behave directly
behave
```

#### 3.2 Advanced Run Options

```bash
# Run smoke tests
python run_tests.py --smoke

# Run regression tests
python run_tests.py --regression

# Generate a test report
python run_tests.py --report

# Generate an Allure report
python run_tests.py --allure

# Run tests in parallel
python run_tests.py --parallel

# Run tests by tag
python run_tests.py --tags "@smoke"
```

#### 3.3 Using the behave Command

```bash
# Run all tests
behave

# Run tests with a specific tag
behave --tags="@smoke"

# Generate a JSON report
behave --format=json --outfile=reports/report.json

# Run in parallel
behave --processes=2
```

## 📝 Writing Test Cases

### 1. Create a Feature File

Create a `.feature` file in the `features/` directory:

```gherkin
# language: en
Feature: Weather Inquiry Functionality
  As a user
  I want to be able to query the weather for different cities
  So that I can understand the weather conditions

  Scenario: Query Beijing Weather
    Given I have opened the My Observatory app
    When I search for the city "Beijing"
    And I select the city "Beijing"
    Then I should see the current temperature information
    And I should see the weather description
```

### 2. Implement Test Steps

Create a step implementation file in the `features/steps/` directory:

```python
from behave import given, when, then
from utils.app_driver import AppDriver

@given('I have opened the My Observatory app')
def step_open_app(context):
    context.driver = AppDriver()
    context.driver.start_driver()

@when('I search for the city "{city_name}"')
def step_search_city(context, city_name):
    # Implement search logic here
    pass
```

### 3. Add Test Data

Create a YAML file in the `test_data/` directory:

```yaml
cities:
  beijing:
    name: "Beijing"
    coordinates:
      latitude: 39.9042
      longitude: 116.4074
```

## 🔧 Configuration Explanation

### 1. Application Configuration (config/config.yaml)

```yaml
# Appium server configuration
appium:
  host: "127.0.0.1"
  port: 4723

# Test environment configuration
environments:
  android:
    platform_name: "Android"
    automation_name: "UiAutomator2"
    device_name: "Android Emulator"
    app_package: "com.weather.forecast.weatherlive"
    app_activity: "com.weather.forecast.weatherlive.MainActivity"
```

### 2. Behave Configuration (behave.ini)

```ini
[behave]
format=pretty
show_skipped=true
show_timings=true
verbose=true
```

## 📊 Test Reports

### 1. Console Report

Detailed execution information will be displayed when running the tests:

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

### 2. HTML Report

```bash
python run_tests.py --report
```

### 3. Allure Report

```bash
# Generate Allure report
python run_tests.py --allure

# View report
allure serve reports/allure-results
```

## 🐛 Troubleshooting

### 1. Appium Connection Problem

```bash
# Check Appium server status
curl http://127.0.0.1:4723/status

# Restart Appium server
appium --reset
```

### 2. Device Connection Problem

```bash
# Check Android device
adb devices

# Check iOS device
xcrun simctl list devices
```

### 3. Element Locating Problem

- Use Appium Inspector to view elements
- Check if element ID is correct
- Confirm application version compatibility

### 4. Common Error Solutions

#### Error: "No such element"

- Check element locator is correct
- Increase waiting time
- Confirm page is fully loaded

#### Error: "Session not created"

- Check device connection status
- Confirm application is installed
- Verify Appium configuration

## 🔄 CI/CD Integration

### 1. GitHub Actions

Project includes two CI configuration files:

#### Main Test Flow (`.github/workflows/appium-test.yml`)

```yaml
name: Appium Automation Test
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  appium-test:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Python 3.9
        uses: actions/setup-python@v4
        with:
          python-version: 3.9
      - name: Install Appium
        run: npm install -g appium@latest
      - name: Run tests
        run: python run_tests.py --report
```

#### Complete Test Flow (`.github/workflows/test.yml`)

Includes multi-Python version testing and Android emulator support.

### 2. Docker Support

#### Build and Run

```bash
# Build image
docker build -t appium-test-framework .

# Use docker-compose to run
docker-compose up --build

# Run container directly
docker run -p 4723:4723 appium-test-framework
```

#### Environment Variables

| Variable Name | Default Value    | Description           |
| ------------- | ---------------- | --------------------- |
| APPIUM_HOST   | 127.0.0.1        | Appium server address |
| APPIUM_PORT   | 4723             | Appium server port    |
| ANDROID_HOME  | /opt/android-sdk | Android SDK path      |

### 3. Local CI/CD Setup

Detailed setup instructions can be found in [CI_CD_SETUP.md](CI_CD_SETUP.md)

### 4. Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Environment') {
            steps {
                sh 'npm install -g appium@latest'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'appium &'
                sh 'sleep 10'
                sh 'python run_tests.py --report'
            }
        }
        stage('Publish Results') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'test_report.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }
}
```

## 📈 Best Practices

### 1. Test Case Design

- Use clear scenario descriptions
- Keep test cases independent
- Use background and scenario outlines reasonably

### 2. Code Organization

- Follow Page Object Model
- Separate test data from test logic
- Use meaningful variable names and function names

### 3. Error Handling

- Add appropriate waiting mechanisms
- Implement failure retry mechanism
- Save detailed error information

### 4. Performance Optimization

- Use parallel execution to improve efficiency
- Optimize element locating strategy
- Reduce unnecessary waiting time

## 🤝 Contribution Guidelines

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Contact Information

If you have any questions or suggestions, please contact us via:

- Project Issues: [GitHub Issues](https://github.com/your-repo/issues)
- Email: your-email@example.com

---

**Note**: Please ensure that Appium environment and test device are correctly configured before use.
