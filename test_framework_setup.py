#!/usr/bin/env python3
"""
框架设置验证脚本
用于检查APP自动化测试框架的环境配置是否正确
"""
import os
import sys
import yaml
import subprocess
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("   需要Python 3.7或更高版本")
        return False


def check_dependencies():
    """检查Python依赖"""
    print("\n🔍 检查Python依赖...")
    required_packages = [
        'behave', 'Appium-Python-Client', 'pytest', 'selenium', 
        'requests', 'PyYAML', 'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 请安装缺失的依赖:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True


def check_appium():
    """检查Appium安装"""
    print("\n🔍 检查Appium...")
    try:
        result = subprocess.run(['appium', '--version'], 
                              capture_output=True, text=True, timeout=10)
        print("result is" + result)
        if result.returncode == 0:
            print(f"✅ Appium已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ Appium未正确安装")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Appium未安装或不在PATH中")
        print("   请运行: npm install -g appium")
        return False


def check_android_sdk():
    """检查Android SDK"""
    print("\n🔍 检查Android SDK...")
    
    # 检查ANDROID_HOME环境变量
    android_home = os.environ.get('ANDROID_HOME')
    if android_home:
        print(f"✅ ANDROID_HOME: {android_home}")
        
        # 检查adb
        adb_path = os.path.join(android_home, 'platform-tools', 'adb')
        if os.path.exists(adb_path):
            print("✅ ADB工具已找到")
            return True
        else:
            print("❌ ADB工具未找到")
            return False
    else:
        print("❌ ANDROID_HOME环境变量未设置")
        print("   请设置Android SDK路径")
        return False


def check_project_structure():
    """检查项目结构"""
    print("\n🔍 检查项目结构...")
    
    required_dirs = [
        'features', 'features/steps', 'features/environment',
        'config', 'test_data', 'utils', 'reports', 'screenshots'
    ]
    
    required_files = [
        'requirements.txt', 'behave.ini', 'run_tests.py', 'README.md',
        'config/config.yaml', 'test_data/weather_data.yaml',
        'features/weather_app.feature', 'features/steps/weather_app_steps.py',
        'features/environment.py', 'utils/app_driver.py',
        'utils/test_data_manager.py', 'utils/page_objects.py'
    ]
    
    all_good = True
    
    # 检查目录
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ 目录: {dir_path}")
        else:
            print(f"❌ 目录缺失: {dir_path}")
            all_good = False
    
    # 检查文件
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ 文件: {file_path}")
        else:
            print(f"❌ 文件缺失: {file_path}")
            all_good = False
    
    return all_good


def check_config_files():
    """检查配置文件"""
    print("\n🔍 检查配置文件...")
    
    # 检查config.yaml
    try:
        with open('config/config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        required_keys = ['appium', 'environments', 'test_data', 'reports']
        for key in required_keys:
            if key in config:
                print(f"✅ 配置项: {key}")
            else:
                print(f"❌ 配置项缺失: {key}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ 配置文件检查失败: {e}")
        return False


def check_test_data():
    """检查测试数据"""
    print("\n🔍 检查测试数据...")
    
    try:
        with open('test_data/weather_data.yaml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        required_keys = ['cities', 'weather_types', 'test_users', 'expected_weather']
        for key in required_keys:
            if key in data:
                print(f"✅ 测试数据: {key}")
            else:
                print(f"❌ 测试数据缺失: {key}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ 测试数据检查失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("我的天文台应用自动化测试框架 - 环境检查")
    print("=" * 60)
    
    checks = [
        ("Python版本", check_python_version),
        ("Python依赖", check_dependencies),
        ("Appium", check_appium),
        ("Android SDK", check_android_sdk),
        ("项目结构", check_project_structure),
        ("配置文件", check_config_files),
        ("测试数据", check_test_data)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name}检查失败: {e}")
            results.append((name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("检查结果总结:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{total} 项检查通过")
    
    if passed == total:
        print("\n🎉 恭喜！框架环境配置正确，可以开始使用。")
        print("\n📝 下一步:")
        print("1. 启动Appium服务器: appium")
        print("2. 连接Android设备或启动模拟器")
        print("3. 运行测试: python run_tests.py")
    else:
        print(f"\n⚠️  有 {total - passed} 项检查未通过，请根据上述提示进行修复。")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 