#!/usr/bin/env python3
"""
My Observatory App Automation Test Runner Script
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime


def run_behave_tests(tags=None, format_type="pretty", parallel=False, output_file=None):
    """
    Run behave tests
    
    Args:
        tags (str): Tag filter
        format_type (str): Output format
        parallel (bool): Whether to run in parallel
        output_file (str): Output file path
    """
    cmd = ["behave"]
    
    # Add tag filter
    if tags:
        cmd.extend(["--tags", tags])
    
    # Add format
    cmd.extend(["--format", format_type])
    
    # Add parallel execution
    if parallel:
        cmd.extend(["--processes", "2"])
    
    # Add output file
    if output_file:
        cmd.extend(["--outfile", output_file])
    
    # Add verbose output
    cmd.append("--verbose")
    
    print(f"Executing command: {' '.join(cmd)}")
    
    try:
        # On Windows, use system default encoding to avoid UTF-8 decoding errors
        if os.name == 'nt':  # Windows
            result = subprocess.run(cmd, check=True, capture_output=True, text=True,
                                    encoding='gbk', errors='ignore')
        else:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True,
                                    encoding='utf-8', errors='ignore')

        print("Tests executed successfully!")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Test execution failed: {e}")
        if e.stdout:
            print("Standard Output:")
            print(e.stdout)
        if e.stderr:
            print("Error Output:")
            print(e.stderr)
        return False
    except UnicodeDecodeError as e:
        print(f"Encoding error: {e}")
        print("Trying to rerun with a different encoding...")
        try:
            # Try not to capture output, just print to console
            result = subprocess.run(cmd, check=True)
            print("Tests executed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Test execution failed: {e}")
            return False


def run_smoke_tests():
    """Run smoke tests"""
    print("Running smoke tests...")
    return run_behave_tests(tags="@smoke", format_type="pretty")


def run_regression_tests():
    """Run regression tests"""
    print("Running regression tests...")
    return run_behave_tests(format_type="pretty")


def run_tests_with_report():
    """Run tests and generate a report"""
    print("Running tests and generating a report...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"reports/test_report_{timestamp}.txt"
    
    # Ensure the reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    return run_behave_tests(
        format_type="pretty",
        output_file=output_file
    )


def run_tests_with_allure():
    """Run tests and generate an Allure report"""
    print("Running tests and generating an Allure report...")
    
    # Ensure the allure results directory exists
    os.makedirs("reports/allure-results", exist_ok=True)
    
    cmd = [
        "behave",
        "--format=allure_behave.formatter:AllureFormatter",
        "--outfile=reports/allure-results"
    ]
    
    try:
        # On Windows, use system default encoding to avoid UTF-8 decoding errors
        if os.name == 'nt':  # Windows
            result = subprocess.run(
                cmd, check=True, encoding='gbk', errors='ignore')
        else:
            result = subprocess.run(
                cmd, check=True, encoding='utf-8', errors='ignore')

        print("Allure report generated successfully!")
        print("Run 'allure serve reports/allure-results' to view the report.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Allure report generation failed: {e}")
        return False
    except UnicodeDecodeError as e:
        print(f"Encoding error: {e}")
        print("Trying to rerun with a different encoding...")
        try:
            result = subprocess.run(cmd, check=True)
            print("Allure report generated successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Allure report generation failed: {e}")
            return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="My Observatory App Automation Test Runner")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--regression", action="store_true", help="Run regression tests")
    parser.add_argument("--report", action="store_true", help="Generate a test report")
    parser.add_argument("--allure", action="store_true", help="Generate an Allure report")
    parser.add_argument("--tags", type=str, help="Specify tag filter")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("My Observatory App Automation Test Framework")
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
        # Default to running all tests
        success = run_behave_tests(parallel=args.parallel)
    
    if success:
        print("\n✅ Tests finished successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test execution failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
