"""
Behave环境配置文件
定义测试执行前后的钩子函数
"""
import os
import time
from datetime import datetime


def before_all(context):
    """在所有测试开始前执行"""
    print("=" * 50)
    print("开始执行我的天文台应用自动化测试")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 创建报告目录
    report_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    # 创建截图目录
    screenshot_dir = os.path.join(os.path.dirname(__file__), "..", "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)


def before_feature(context, feature):
    """在每个特性文件开始前执行"""
    print(f"\n开始执行特性: {feature.name}")
    context.feature_start_time = time.time()


def before_scenario(context, scenario):
    """在每个场景开始前执行"""
    print(f"  - 开始执行场景: {scenario.name}")
    context.scenario_start_time = time.time()
    context.scenario_name = scenario.name


def after_scenario(context, scenario):
    """在每个场景结束后执行"""
    scenario_duration = time.time() - context.scenario_start_time
    print(f"  - 场景执行完成: {scenario.name} (耗时: {scenario_duration:.2f}秒)")
    
    # 如果场景失败，截图
    if scenario.status == "failed":
        if hasattr(context, 'driver') and context.driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"failed_{context.scenario_name}_{timestamp}.png"
            context.driver.take_screenshot(filename)
            print(f"  - 失败截图已保存: {filename}")


def after_feature(context, feature):
    """在每个特性文件结束后执行"""
    feature_duration = time.time() - context.feature_start_time
    print(f"特性执行完成: {feature.name} (耗时: {feature_duration:.2f}秒)")


def after_all(context):
    """在所有测试结束后执行"""
    print("=" * 50)
    print("我的天文台应用自动化测试执行完成")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 清理资源
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit_driver()


def before_step(context, step):
    """在每个步骤开始前执行"""
    print(f"    - 执行步骤: {step.name}")


def after_step(context, step):
    """在每个步骤结束后执行"""
    if step.status == "failed":
        print(f"    - 步骤失败: {step.name}")
        # 可以在这里添加更多失败处理逻辑
    elif step.status == "passed":
        print(f"    - 步骤通过: {step.name}")
    else:
        print(f"    - 步骤跳过: {step.name}") 