"""
Behave environment configuration file.
Defines hook functions to be executed before and after test execution.
"""
import os
import time
from datetime import datetime


def before_all(context):
    """Executed before all tests start."""
    print("=" * 50)
    print("Starting My Observatory App Automation Tests")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Create reports directory
    report_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    # Create screenshots directory
    screenshot_dir = os.path.join(os.path.dirname(__file__), "..", "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)


def before_feature(context, feature):
    """Executed before each feature file."""
    print(f"\nStarting feature: {feature.name}")
    context.feature_start_time = time.time()


def before_scenario(context, scenario):
    """Executed before each scenario."""
    print(f"  - Starting scenario: {scenario.name}")
    context.scenario_start_time = time.time()
    context.scenario_name = scenario.name


def after_scenario(context, scenario):
    """Executed after each scenario."""
    scenario_duration = time.time() - context.scenario_start_time
    print(f"  - Scenario finished: {scenario.name} (Duration: {scenario_duration:.2f}s)")
    
    # Take a screenshot if the scenario fails
    if scenario.status == "failed":
        if hasattr(context, 'driver') and context.driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"failed_{context.scenario_name}_{timestamp}.png"
            context.driver.take_screenshot(filename)
            print(f"  - Failure screenshot saved: {filename}")


def after_feature(context, feature):
    """Executed after each feature file."""
    feature_duration = time.time() - context.feature_start_time
    print(f"Feature finished: {feature.name} (Duration: {feature_duration:.2f}s)")


def after_all(context):
    """Executed after all tests are finished."""
    print("=" * 50)
    print("My Observatory App Automation Tests Finished")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Clean up resources
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit_driver()


def before_step(context, step):
    """Executed before each step."""
    print(f"    - Executing step: {step.name}")


def after_step(context, step):
    """Executed after each step."""
    if step.status == "failed":
        print(f"    - Step failed: {step.name}")
        # More failure handling logic can be added here
    elif step.status == "passed":
        print(f"    - Step passed: {step.name}")
    else:
        print(f"    - Step skipped: {step.name}") 