#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hong Kong Observatory API Definition
========================
"""

import requests
import json
from datetime import datetime, timedelta
from behave import when, then
import time


class WeatherAPIContext:
    """API test context"""

    def __init__(self):
        self.base_url = None
        self.api_url = None
        self.response = None
        self.status_code = None
        self.response_data = None
        self.relative_humidity = None

    def reset(self):
        """reset context"""
        self.response = None
        self.status_code = None
        self.response_data = None
        self.relative_humidity = None


# Global context
api_context = WeatherAPIContext()


@when('I get API of 9-day forcast from Hong Kong Observatory')
def step_get_api_url(context):
    print("Setting the API URL")

    api_context.base_url = "https://data.weather.gov.hk"
    api_context.api_url = f"{api_context.base_url}/weatherAPI/opendata/weather.php"

    params = {
        'dataType': 'fnd',  # 9-day forecast
        'lang': 'en'        
    }

    param_string = "&".join([f"{k}={v}" for k, v in params.items()])
    api_context.full_url = f"{api_context.api_url}?{param_string}"

    print(f"API URL: {api_context.full_url}")

    # Save to context
    context.api_url = api_context.full_url
    context.api_params = params

    print("API URL set up completed")


@then('I send request to the API')
def step_send_request(context):
    """Step 2: Send HTTP request"""
    print("Sending HTTP request to Hong Kong Observatory API")

    try:
        headers = {
            'User-Agent': 'MyObservatory-Test-Framework/1.0',
            'Accept': 'application/json',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8'
        }

        print(f"Request URL: {api_context.full_url}")
        print(f"Request headers: {headers}")

        start_time = time.time()
        api_context.response = requests.get(
            api_context.full_url,
            headers=headers,
            timeout=30
        )
        end_time = time.time()

        api_context.status_code = api_context.response.status_code

        print(f"Request time: {end_time - start_time:.2f}s")
        print(f"Response status code: {api_context.status_code}")
        print(f"Response size: {len(api_context.response.content)} bytes")

        # Save to context
        context.api_response = api_context.response
        context.response_time = end_time - start_time

        print("HTTP request sent successfully")

    except requests.RequestException as e:
        print(f"HTTP request failed: {e}")
        api_context.response = None
        api_context.status_code = None
        context.api_response = None
        raise AssertionError(f"API request failed: {e}")


@then('I check response status is successful')
def step_check_status(context):
    print("Checking API response status code")

    if api_context.response is None:
        raise AssertionError("No API response received")

    status_code = api_context.status_code
    print(f"Actual status code: {status_code}")

    # Check if status code is successful
    if status_code == 200:
        print("Status code check passed - 200 OK")

        # Try to parse JSON response
        try:
            api_context.response_data = api_context.response.json()
            print("JSON response parsed successfully")
            print(f"Response data keys: {list(api_context.response_data.keys())}")

            # Save to context
            context.api_data = api_context.response_data

        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {e}")
            print(f"Raw response: {api_context.response.text[:500]}...")
            raise AssertionError(f"API response is not valid JSON: {e}")

    elif status_code in [404, 403, 401]:
        error_msg = f"API access denied - status code: {status_code}"
        print(f"{error_msg}")
        raise AssertionError(error_msg)

    elif status_code >= 500:
        error_msg = f"Server error - status code: {status_code}"
        print(f"{error_msg}")
        raise AssertionError(error_msg)

    else:
        error_msg = f"Unexpected status code: {status_code}"
        print(f"{error_msg}")
        raise AssertionError(error_msg)


@then('I extract the relative humidity for the day after tommorrow')
def step_extract_humidity(context):
    """Step 4: Extract the relative humidity for the day after tomorrow"""
    print("Extracting the relative humidity for the day after tomorrow")

    if api_context.response_data is None:
        raise AssertionError("No available API response data")

    try:
        # Get today's date
        today = datetime.now().date()
        day_after_tomorrow = today + timedelta(days=2)

        print(f"Today: {today}")
        print(f"Day after tomorrow: {day_after_tomorrow}")
        day_after_tomorrow = str(day_after_tomorrow).replace("-", "")
        print(f"Day after tomorrow: {day_after_tomorrow}")


        # Find 9-day forecast data
        forecast_data = api_context.response_data.get('weatherForecast', [])

        if not forecast_data:
            raise AssertionError("No weather forecast data found in API response")

        print(f"Found {len(forecast_data)} days of forecast data")

        target_forecast = None
        for day_data in forecast_data:
            forecast_date_str = day_data.get('forecastDate')
            if forecast_date_str:
                try:
                    forecast_date = datetime.strptime(
                        forecast_date_str, '%Y%m%d').date()

                    if forecast_date == day_after_tomorrow:
                        target_forecast = day_data
                        break

                except ValueError:
                    try:
                        forecast_date = datetime.strptime(
                            forecast_date_str, '%Y-%m-%d').date()
                        if forecast_date == day_after_tomorrow:
                            target_forecast = day_data
                            break
                    except ValueError:
                        continue

        if target_forecast is None:
            print("No specific forecast data found for the day after tomorrow, using the 3rd day's data")
            if len(forecast_data) >= 3:
                target_forecast = forecast_data[2]  # 3rd day (index 2)
            else:
                raise AssertionError("Insufficient forecast data to get the day after tomorrow's data")
        # check if target_forecast has this type of schema
        # 			"forecastMaxrh": {
			# 	"value": 95,
			# 	"unit": "percent"
			# },
			# "forecastMinrh": {
			# 	"value": 75,
			# 	"unit": "percent"
			# }
        print(target_forecast)
        if target_forecast.get("forecastMinrh") != None and target_forecast.get("forecastMaxrh") != None:
            try: 
                min_humidity = target_forecast['forecastMinrh']['value']
                max_humidity = target_forecast['forecastMaxrh']['value']
                api_context.relative_humidity = f"{min_humidity}% - {max_humidity}%"
                print(f"Relative humidity for the day after tomorrow: {api_context.relative_humidity}")
            except ValueError: 
                print(f"Schema Error")    

        # Save to context
        context.relative_humidity = api_context.relative_humidity
        context.target_date = day_after_tomorrow
        context.forecast_data = target_forecast

        print("Relative humidity extraction successful")

        # Optional: save to file
        save_result_to_file(context)

    except Exception as e:
        print(f"Failed to extract relative humidity: {e}")
        raise AssertionError(f"Unable to extract relative humidity for the day after tomorrow: {e}")


def save_result_to_file(context):
    """Save result to file"""
    try:
        result_data = {
            "api_url": getattr(context, 'api_url', None),
            "response_time": getattr(context, 'response_time', None),
            "status_code": getattr(context.api_response, 'status_code', None) if hasattr(context, 'api_response') else None,
            "relative_humidity": getattr(context, 'relative_humidity', None),
            "target_date": str(getattr(context, 'target_date', '')),
            "forecast_data": getattr(context, 'forecast_data', None),
        }
        # Convert all Status objects to string in forecast_data if present
        if result_data["forecast_data"] and isinstance(result_data["forecast_data"], dict):
            for k, v in result_data["forecast_data"].items():
                if hasattr(v, 'name') and 'Status' in str(type(v)):
                    result_data["forecast_data"][k] = str(v)
        # Save to JSON file
        import os
        os.makedirs('reports', exist_ok=True)
        filename = f"reports/api_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        print(f"Result saved to: {filename}")
    except Exception as e:
        print(f"Failed to save result file: {e}")


# Helper function: Reset API context
def reset_api_context():
    """Reset API test context"""
    api_context.reset()


# Reset context before scenario
def before_scenario(context, scenario):
    """Scenario start hook"""
    reset_api_context()


# Helper function: Display API response summary
@then('I display API response summary')
def step_display_summary(context):
    """Display API response summary (optional step)"""
    print("\n" + "="*50)
    print("API response summary")
    print("="*50)

    if hasattr(context, 'api_url'):
        print(f"API URL: {context.api_url}")

    if hasattr(context, 'response_time'):
        print(f"Response time: {context.response_time:.2f}s")

    if api_context.status_code:
        print(f"Status code: {api_context.status_code}")

    if hasattr(context, 'relative_humidity'):
        print(f"Relative humidity for the day after tomorrow: {context.relative_humidity}")

    if hasattr(context, 'target_date'):
        print(f"Target date: {context.target_date}")

    print("="*50)
