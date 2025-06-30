"""
Step implementations for the My Observatory app tests.
"""
from behave import given, when, then, step
from utils.app_driver import AppDriver
from utils.test_data_manager import TestDataManager
from utils.page_objects import MainPage, SearchPage, MenuPage, SettingsPage
import time


@given('I have opened the My Observatory app')
def step_open_weather_app(context):
    """Opens the My Observatory app."""
    context.driver = AppDriver(platform="android")
    context.driver.start_driver()
    context.main_page = MainPage(context.driver)
    context.test_data = TestDataManager()
    
    # Wait for the app to load completely
    time.sleep(3)


@given('I am on the main page')
def step_on_main_page(context):
    """Confirms that the current page is the main page."""
    # Check if a key element of the main page exists
    assert context.driver.is_element_present(context.main_page.SEARCH_BUTTON), "Search button not found, not on the main page."


@when('I click the search button')
def step_click_search_button(context):
    """Clicks the search button."""
    context.main_page.click_search()
    context.search_page = SearchPage(context.driver)
    time.sleep(2)


@when('I search for the city "{city_name}"')
def step_search_city(context, city_name):
    """Searches for a specific city."""
    context.search_page.search_city(city_name)
    time.sleep(2)


@when('I select the city "{city_name}"')
def step_select_city(context, city_name):
    """Selects a specific city from the search results."""
    context.search_page.select_city(city_name)
    time.sleep(2)


@when('I click the location button')
def step_click_location_button(context):
    """Clicks the location button to get weather for the current location."""
    context.main_page.click_location()
    time.sleep(3)


@when('I click the menu button')
def step_click_menu_button(context):
    """Clicks the menu button."""
    context.main_page.click_menu()
    context.menu_page = MenuPage(context.driver)
    time.sleep(2)


@when('I click the settings button')
def step_click_settings_button(context):
    """Clicks the settings button."""
    context.menu_page.click_settings()
    context.settings_page = SettingsPage(context.driver)
    time.sleep(2)


@when('I toggle the temperature unit')
def step_toggle_temperature_unit(context):
    """Toggles the temperature unit setting."""
    context.settings_page.toggle_temperature_unit()
    time.sleep(1)


@when('I toggle the notification settings')
def step_toggle_notification(context):
    """Toggles the notification setting."""
    context.settings_page.toggle_notification()
    time.sleep(1)


@then('I should see the current temperature information')
def step_see_current_temperature(context):
    """Verifies that the current temperature is displayed."""
    temperature = context.main_page.get_current_temperature()
    assert temperature is not None, "Temperature information not found."
    assert context.test_data.validate_temperature(temperature), f"Temperature value {temperature} is not within a reasonable range."


@then('I should see the weather description')
def step_see_weather_description(context):
    """Verifies that the weather description is displayed."""
    description = context.main_page.get_weather_description()
    assert description, "Weather description not found."
    assert len(description) > 0, "Weather description is empty."


@then('I should see the humidity information')
def step_see_humidity_info(context):
    """Verifies that the humidity information is displayed."""
    humidity = context.main_page.get_humidity()
    assert humidity is not None, "Humidity information not found."
    assert context.test_data.validate_humidity(humidity), f"Humidity value {humidity} is not within a reasonable range."


@then('I should see the wind speed information')
def step_see_wind_speed_info(context):
    """Verifies that the wind speed information is displayed."""
    wind_speed = context.main_page.get_wind_speed()
    assert wind_speed is not None, "Wind speed information not found."
    wind_range = context.test_data.get_expected_weather_range().get("wind_speed_range", {})
    min_wind = wind_range.get("min", 0)
    max_wind = wind_range.get("max", 100)
    assert min_wind <= wind_speed <= max_wind, f"Wind speed value {wind_speed} is not within a reasonable range."


@then('the search page should be displayed')
def step_search_page_should_display(context):
    """Verifies that the search page is displayed."""
    assert context.driver.is_element_present(context.search_page.SEARCH_INPUT), "Search input not found, not on the search page."


@then('the city "{city_name}" should be selected')
def step_city_should_be_selected(context, city_name):
    """Verifies that the correct city is selected."""
    # This can be verified by checking the page title or another identifier
    time.sleep(2)
    # Verification logic can be added based on the actual app's elements.


@then('the settings page should be displayed')
def step_settings_page_should_display(context):
    """Verifies that the settings page is displayed."""
    assert context.driver.is_element_present(context.settings_page.TEMPERATURE_UNIT_TOGGLE), "Temperature unit toggle not found, not on the settings page."


@step('I close the app')
def step_close_app(context):
    """Closes the application."""
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit_driver()


# Steps for data-driven testing
@given('I use the city "{city_key}" from the test data')
def step_use_test_city(context, city_key):
    """Uses a city from the test data file."""
    context.city_data = context.test_data.get_city_data(city_key)
    context.city_name = context.test_data.get_city_name(city_key)
    assert context.city_name, f"City data not found for key: {city_key}"


@then('the temperature should be within a reasonable range')
def step_temperature_should_be_reasonable(context):
    """Verifies that the temperature is within a reasonable range."""
    temperature = context.main_page.get_current_temperature()
    assert context.test_data.validate_temperature(temperature), f"Temperature {temperature} is not within a reasonable range."


@then('the humidity should be within a reasonable range')
def step_humidity_should_be_reasonable(context):
    """Verifies that the humidity is within a reasonable range."""
    humidity = context.main_page.get_humidity()
    assert context.test_data.validate_humidity(humidity), f"Humidity {humidity} is not within a reasonable range." 