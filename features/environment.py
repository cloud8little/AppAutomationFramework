"""
Behave environment configuration file.
Defines hook functions to be executed before and after test execution.
"""
import os
import time
import json
from datetime import datetime
from steps.weather_api_steps import reset_api_context


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
    screenshot_dir = os.path.join(
        os.path.dirname(__file__), "..", "screenshots")
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

    # Reset API context for each scenario
    reset_api_context()

    # Initialize scenario-specific attributes
    context.api_response = None
    context.api_data = None
    context.relative_humidity = None


def after_scenario(context, scenario):
    """Executed after each scenario."""
    scenario_duration = time.time() - context.scenario_start_time

    # Save API test results to JSON file
    if hasattr(context, 'api_response') and context.api_response:
        save_api_test_result(context, scenario)

    # Take a screenshot if the scenario fails and driver is available
    if scenario.status == "failed":
        if hasattr(context, 'driver') and context.driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"failed_{context.scenario_name}_{timestamp}.png"
            context.driver.take_screenshot(filename)
            print(f"  - Failure screenshot saved: {filename}")


def save_api_test_result(context, scenario):
    """Save API test results to JSON file."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"status", scenario.status)
        result_data = {
            'scenario_name': scenario.name,
            'status': str(scenario.status),
            'timestamp': datetime.now().isoformat(),
            'duration': time.time() - context.scenario_start_time,
            'api_url': getattr(context, 'api_url', None),
            'status_code': getattr(context.api_response, 'status_code', None) if hasattr(context, 'api_response') else None,
            'response_time': getattr(context, 'response_time', None),
            'relative_humidity': getattr(context, 'relative_humidity', None),
            'target_date': str(getattr(context, 'target_date', None)),
        }

        # Save to reports directory
        filename = f"reports/api_test_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)

        print(f"API test result saved: {filename}")

    except Exception as e:
        print(f"Failed to save API test result: {e}")


def after_feature(context, feature):
    """Executed after each feature file."""
    feature_duration = time.time() - context.feature_start_time
    print(
        f"Feature finished: {feature.name} (Duration: {feature_duration:.2f}s)")


def after_all(context):
    """Executed after all tests are finished."""
    print("=" * 50)
    print("My Observatory App Automation Tests Finished")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Clean up resources
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit_driver()

    # Print Behave built-in statistics (robust version)
    runner = getattr(context, '_runner', None)
    if runner and hasattr(runner, 'features'):
        features = runner.features
        total_features = len(features)
        total_scenarios = sum(len(f.scenarios) for f in features)
        passed_scenarios = sum(
            1 for f in features for s in f.scenarios if getattr(s.status, 'name', s.status) == "passed"
        )
        failed_scenarios = sum(
            1 for f in features for s in f.scenarios if getattr(s.status, 'name', s.status) == "failed"
        )
        total_steps = sum(len(s.steps) for f in features for s in f.scenarios)
        passed_steps = sum(
            1 for f in features for s in f.scenarios for step in s.steps if getattr(step.status, 'name', step.status) == "passed"
        )
        failed_steps = sum(
            1 for f in features for s in f.scenarios for step in s.steps if getattr(step.status, 'name', step.status) == "failed"
        )
        skipped_steps = sum(
            1 for f in features for s in f.scenarios for step in s.steps if getattr(step.status, 'name', step.status) == "skipped"
        )

        print(f"Total features: {total_features}")
        print(f"Total scenarios: {total_scenarios}")
        print(f"Passed scenarios: {passed_scenarios}")
        print(f"Failed scenarios: {failed_scenarios}")
        print(f"Total steps: {total_steps}")
        print(f"Passed steps: {passed_steps}")
        print(f"Failed steps: {failed_steps}")
        print(f"Skipped steps: {skipped_steps}")


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
