#!/usr/bin/env python3
"""
我的天文台应用自动化测试运行脚本
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime


def run_behave_tests(tags=None, format_type="pretty", parallel=False, output_file=None):
    """
    运行behave测试
    
    Args:
        tags (str): 标签过滤
        format_type (str): 输出格式
        parallel (bool): 是否并行执行
        output_file (str): 输出文件
    """
    cmd = ["behave"]
    
    # 添加标签过滤
    if tags:
        cmd.extend(["--tags", tags])
    
    # 添加格式
    cmd.extend(["--format", format_type])
    
    # 添加并行执行
    if parallel:
        cmd.extend(["--processes", "2"])
    
    # 添加输出文件
    if output_file:
        cmd.extend(["--outfile", output_file])
    
    # 添加详细输出
    cmd.append("--verbose")
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("测试执行成功!")
        if result.stdout:
            print("输出:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"测试执行失败: {e}")
        if e.stdout:
            print("标准输出:")
            print(e.stdout)
        if e.stderr:
            print("错误输出:")
            print(e.stderr)
        return False


def run_smoke_tests():
    """运行冒烟测试"""
    print("运行冒烟测试...")
    return run_behave_tests(tags="@smoke", format_type="pretty")


def run_regression_tests():
    """运行回归测试"""
    print("运行回归测试...")
    return run_behave_tests(format_type="pretty")


def run_tests_with_report():
    """运行测试并生成报告"""
    print("运行测试并生成报告...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"reports/test_report_{timestamp}.txt"
    
    # 确保报告目录存在
    os.makedirs("reports", exist_ok=True)
    
    return run_behave_tests(
        format_type="pretty",
        output_file=output_file
    )


def run_tests_with_allure():
    """运行测试并生成Allure报告"""
    print("运行测试并生成Allure报告...")
    
    # 确保报告目录存在
    os.makedirs("reports/allure-results", exist_ok=True)
    
    cmd = [
        "behave",
        "--format=allure_behave.formatter:AllureFormatter",
        "--outfile=reports/allure-results"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("Allure报告生成成功!")
        print("运行 'allure serve reports/allure-results' 查看报告")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Allure报告生成失败: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="我的天文台应用自动化测试运行器")
    parser.add_argument("--smoke", action="store_true", help="运行冒烟测试")
    parser.add_argument("--regression", action="store_true", help="运行回归测试")
    parser.add_argument("--report", action="store_true", help="生成测试报告")
    parser.add_argument("--allure", action="store_true", help="生成Allure报告")
    parser.add_argument("--tags", type=str, help="指定标签过滤")
    parser.add_argument("--parallel", action="store_true", help="并行执行测试")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("我的天文台应用自动化测试框架")
    print("=" * 60)
    
    success = False
    
    if args.smoke:
        success = run_smoke_tests()
    elif args.regression:
        success = run_regression_tests()
    elif args.report:
        success = run_tests_with_report()
    elif args.allure:
        success = run_tests_with_allure()
    elif args.tags:
        success = run_behave_tests(tags=args.tags, parallel=args.parallel)
    else:
        # 默认运行所有测试
        success = run_behave_tests(parallel=args.parallel)
    
    if success:
        print("\n✅ 测试执行完成!")
        sys.exit(0)
    else:
        print("\n❌ 测试执行失败!")
        sys.exit(1)


if __name__ == "__main__":
    main() 