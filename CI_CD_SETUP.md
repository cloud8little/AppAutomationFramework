# CI/CD Setup Guide

This document describes how to set up and configure the CI/CD pipeline for automated testing.

## 📋 Table of Contents

- [GitHub Actions Configuration](#github-actions-configuration)
- [Docker Environment](#docker-environment)
- [Local Development](#local-development)
- [Troubleshooting](#troubleshooting)

## 🚀 GitHub Actions Configuration

### 1. Automatic Triggers

The CI/CD pipeline is automatically triggered in the following cases:

- Pushing to the `main` or `develop` branch
- Creating a Pull Request to the `main` branch
- Manual trigger (workflow_dispatch)

### 2. Workflows

The project includes three different CI configuration files for different scenarios:

#### Simplified Test Flow (`.github/workflows/simple-test.yml`) - Recommended

Suitable for basic Appium tests, does not include the Android SDK:

- ✅ Quick start
- ✅ Minimal dependencies
- ✅ Suitable for verifying basic functionality

#### Standard Test Flow (`.github/workflows/appium-test.yml`)

Includes a complete Appium environment:

- ✅ Appium server
- ✅ Basic system dependencies
- ✅ Suitable for most testing scenarios

#### Complete Test Flow (`.github/workflows/test.yml`)

Includes Android SDK and emulator support:

- ✅ Multi-Python version testing
- ✅ Android SDK environment
- ✅ Emulator support
- ⚠️ Longer build times

### 3. Recommended Configuration

For most projects, it is recommended to use the **Simplified Test Flow**:

1. Create the `.github/workflows/` directory in your GitHub repository.
2. Copy `simple-test.yml` to this directory.
3. Commit and push the changes.

If you need Android SDK support, you can use `appium-test.yml` or `test.yml`.

## 🐳 Docker Environment

### 1. Build the Image

```bash
docker build -t appium-test-framework .
```

### 2. Run the Container

```bash
# Using docker-compose (recommended)
docker-compose up --build

# Or using docker directly
docker run -p 4723:4723 -v $(pwd)/reports:/app/reports appium-test-framework
```

### 3. Environment Variables

| Variable Name    | Default Value    | Description           |
| ---------------- | ---------------- | --------------------- |
| APPIUM_HOST      | 127.0.0.1        | Appium server address |
| APPIUM_PORT      | 4723             | Appium server port    |
| ANDROID_HOME     | /opt/android-sdk | Android SDK path      |
| ANDROID_SDK_ROOT | /opt/android-sdk | Android SDK root path |

## 💻 Local Development

### 1. Environment Requirements

- Python 3.8+
- Node.js 16+
- Java 11+
- Android SDK

### 2. Installation Steps

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Appium
npm install -g appium@latest
npm install -g appium-doctor

# 3. Verify installation
appium --version
appium-doctor --android
```

### 3. Running Tests

```bash
# Start the Appium server
appium &

# Run the tests
python run_tests.py --report
```

## 🔧 Troubleshooting

### 1. Appium Connection Issues

**Problem**: Cannot connect to the Appium server.
**Solution**:

```bash
# Check Appium status
curl http://127.0.0.1:4723/status

# Restart Appium
pkill -f appium
appium --reset
```

### 2. Android SDK Issues

**Problem**: Android SDK not found.
**Solution**:

```bash
# Set environment variables
export ANDROID_HOME=/path/to/android-sdk
export ANDROID_SDK_ROOT=/path/to/android-sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Verify installation
adb version
```

### 3. Permission Issues

**Problem**: Insufficient permissions in the Docker container.
**Solution**:

```bash
# Run in privileged mode
docker run --privileged -p 4723:4723 appium-test-framework
```

### 4. Network Issues

**Problem**: Cannot download dependencies.
**Solution**:

```bash
# Use a regional mirror
npm config set registry https://registry.npmmirror.com
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 📊 Monitoring and Reporting

### 1. Test Reports

- **HTML Report**: `reports/test_report.html`
- **Allure Report**: `reports/allure-results/`
- **Screenshots**: `screenshots/`

### 2. Log Files

- **Appium Log**: `appium.log`
- **Test Log**: `reports/test.log`

### 3. Performance Metrics

- Test execution time
- Success rate
- Failure reason analysis

## 🔄 CI Best Practices

### 1. Parallel Execution

Use a matrix strategy to test multiple Python versions in parallel:

```yaml
strategy:
  matrix:
    python-version: [3.8, 3.9, "3.10"]
```

### 2. Cache Optimization

Cache dependencies to speed up builds:

```yaml
- name: Cache Python dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### 3. Conditional Execution

Run tests only under specific conditions:

```yaml
- name: Run tests
  if: github.event_name == 'push' || github.event_name == 'pull_request'
  run: python run_tests.py
```

## 📞 Support

If you have any issues, please:

1. Check the GitHub Actions logs.
2. Verify your local environment configuration.
3. Submit an issue to the project repository.

---

**Note**: Ensure that all necessary environment variables and dependencies are correctly configured in your CI/CD environment.
