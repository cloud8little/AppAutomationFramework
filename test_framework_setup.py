#!/usr/bin/env python3
"""
Framework Setup Validation Script
Used to check if the environment for the APP automation test framework is configured correctly.
"""
import os
import sys
import yaml
import subprocess
from pathlib import Path


def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version too low: {version.major}.{version.minor}.{version.micro}")
        print("   Python 3.7 or higher is required.")
        return False


def check_dependencies():
    """Check Python dependencies"""
    print("\n🔍 Checking Python dependencies...")
    # Mapping of package names to actual import module names
    package_imports = {
        'behave': 'behave',
        'Appium-Python-Client': 'appium',
        'pytest': 'pytest',
        'selenium': 'selenium',
        'requests': 'requests',
        'PyYAML': 'yaml',
        'python-dotenv': 'dotenv'
    }
    
    missing_packages = []
    for package, import_name in package_imports.items():
        try:
            __import__(import_name)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package} - Not installed, error: {e}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Please install the missing dependencies:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True


def check_appium():
    """Check Appium installation"""
    print("\n🔍 Checking Appium...")
    
    # On Windows, try multiple possible appium paths
    appium_commands = ['appium', 'npx appium']
    
    # Common paths for npm global install on Windows
    if os.name == 'nt':  # Windows system
        try:
            print("🔍 Getting npm global install path...")
            npm_prefix = subprocess.run(['npm', 'config', 'get', 'prefix'],
                                        capture_output=True, text=True, timeout=10)
            print(f"📝 npm command return code: {npm_prefix.returncode}")

            if npm_prefix.returncode == 0:
                npm_path = npm_prefix.stdout.strip()
                print(f"✅ npm global path: {npm_path}")

                # Add more possible paths
                additional_paths = [
                    os.path.join(npm_path, 'appium.cmd'),
                    os.path.join(npm_path, 'appium.ps1'),
                    os.path.join(npm_path, 'node_modules',
                                 '.bin', 'appium.cmd'),
                    os.path.join(npm_path, 'node_modules', '.bin', 'appium'),
                    os.path.join(os.environ.get('APPDATA', ''),
                                 'npm', 'appium.cmd'),
                    os.path.join(os.environ.get(
                        'APPDATA', ''), 'npm', 'appium')
                ]

                # Check which paths actually exist
                existing_paths = []
                for path in additional_paths:
                    if os.path.exists(path):
                        existing_paths.append(path)
                        print(f"✅ Found Appium path: {path}")

                appium_commands.extend(existing_paths)
            else:
                print(f"❌ npm command execution failed, error output: {npm_prefix.stderr}")

        except FileNotFoundError:
            print("❌ npm command not found, Node.js may not be installed or added to PATH.")
            print("   Please install Node.js first: https://nodejs.org/")
            print("   Or check if the Node.js installation path is in the PATH environment variable.")
            
            # Try common npm installation paths
            print("🔍 Trying to check common npm installation paths...")
            common_npm_paths = [
                r"C:\Program Files\nodejs",
                r"C:\Program Files (x86)\nodejs", 
                os.path.join(os.environ.get('APPDATA', ''), 'npm'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'npm'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Roaming', 'npm')
            ]
            
            for npm_path in common_npm_paths:
                if os.path.exists(npm_path):
                    print(f"✅ Found possible npm path: {npm_path}")
                    appium_paths = [
                         os.path.join(npm_path, 'appium.cmd'),
                         os.path.join(npm_path, 'appium.ps1'),
                         os.path.join(npm_path, 'node_modules', '.bin', 'appium.cmd'),
                         os.path.join(npm_path, 'node_modules', '.bin', 'appium')
                    ]
                    
                    for path in appium_paths:
                        if os.path.exists(path):
                            appium_commands.append(path)
                            print(f"✅ Found Appium path: {path}")
            
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"❌ Failed to get npm prefix: {e}")
        except Exception as e:
            print(f"❌ An unknown error occurred while checking npm path: {e}")

    print(f"📝 Will try the following Appium commands: {appium_commands}")

    for appium_cmd in appium_commands:
        try:
            print(f"Attempting to execute: {appium_cmd}")

            # For commands with spaces, need to split them
            if isinstance(appium_cmd, str) and ' ' in appium_cmd:
                cmd_parts = appium_cmd.split()
            else:
                cmd_parts = [appium_cmd]

            result = subprocess.run(cmd_parts + ['--version'],
                                     capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Appium is installed: {result.stdout.strip()}")
                print(f"   Using path: {appium_cmd}")
                return True
            else:
                print(f"❌ Command execution failed: {appium_cmd}")
                print(f"   Error output: {result.stderr}")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"❌ Command not found or timed out: {appium_cmd}, error: {e}")
            continue
        except Exception as e:
            print(f"❌ An unknown error occurred while executing command: {appium_cmd}, error: {e}")
            continue

    print("❌ All Appium path attempts failed.")
    print("   Please run: npm install -g appium")
    print("   Or check if the npm global installation path is in the PATH environment variable.")
    print("   It is recommended to manually check the following paths:")
    user_profile = os.environ.get('USERPROFILE', 'C:\\Users\\<YourUser>')
    roaming_npm = os.path.join(user_profile, 'AppData', 'Roaming', 'npm')
    print(f"   - {os.path.join(os.environ.get('APPDATA', ''), 'npm')}")
    print(f"   - {roaming_npm}")
    return False


def check_android_sdk():
    """Check Android SDK"""
    print("\n🔍 Checking Android SDK...")
    
    # Check ANDROID_HOME environment variable
    android_home = os.environ.get('ANDROID_HOME')
    if android_home:
        print(f"✅ ANDROID_HOME: {android_home}")
        
        # Check for adb
        adb_path = os.path.join(android_home, 'platform-tools', 'adb')
        if os.path.exists(adb_path):
            print("✅ ADB tool found.")
            return True
        else:
            print("❌ ADB tool not found.")
            return False
    else:
        print("❌ ANDROID_HOME environment variable not set.")
        print("   Please set the path to your Android SDK.")
        return False


def check_project_structure():
    """Check project structure"""
    print("\n🔍 Checking project structure...")
    
    required_dirs = [
        'features', 'features/steps',
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
    
    # Check directories
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Directory: {dir_path}")
        else:
            print(f"❌ Missing directory: {dir_path}")
            all_good = False
    
    # Check files
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ File: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            all_good = False
    
    return all_good


def check_config_files():
    """Check configuration files"""
    print("\n🔍 Checking configuration files...")
    
    # Check config.yaml
    try:
        with open('config/config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        required_keys = ['appium', 'environments', 'test_data', 'reports']
        for key in required_keys:
            if key in config:
                print(f"✅ Config key: {key}")
            else:
                print(f"❌ Missing config key: {key}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Config file check failed: {e}")
        return False


def check_test_data():
    """Check test data"""
    print("\n🔍 Checking test data...")
    
    try:
        with open('test_data/weather_data.yaml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        required_keys = ['cities', 'weather_types',
                         'test_users', 'expected_weather']
        for key in required_keys:
            if key in data:
                print(f"✅ Test data key: {key}")
            else:
                print(f"❌ Missing test data key: {key}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Test data check failed: {e}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("My Observatory App Automation Test Framework - Environment Check")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Python Dependencies", check_dependencies),
        ("Appium", check_appium),
        ("Android SDK", check_android_sdk),
        ("Project Structure", check_project_structure),
        ("Configuration Files", check_config_files),
        ("Test Data", check_test_data)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Check Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ Passed" if result else "❌ Failed"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} checks passed.")
    
    if passed == total:
        print("\n🎉 Congratulations! Framework environment is configured correctly. You can start.")
        print("\n📝 Next steps:")
        print("1. Start the Appium server: appium")
        print("2. Connect an Android device or start an emulator")
        print("3. Run tests: python run_tests.py")
    else:
        print(f"\n⚠️  {total - passed} checks failed. Please fix them according to the prompts above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
