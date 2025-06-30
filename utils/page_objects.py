"""
Page Object Model for the My Observatory app.
"""
from appium.webdriver.common.appiumby import AppiumBy
from utils.app_driver import AppDriver


class BasePage:
    """Base Page Class"""
    
    def __init__(self, driver: AppDriver):
        self.driver = driver
    
    def wait_for_element(self, locator, timeout=None):
        """Waits for an element to appear."""
        return self.driver.find_element(locator, timeout)
    
    def click_element(self, locator, timeout=None):
        """Clicks an element."""
        self.driver.click_element(locator, timeout)
    
    def input_text(self, locator, text, timeout=None):
        """Inputs text into an element."""
        self.driver.input_text(locator, text, timeout)
    
    def get_text(self, locator, timeout=None):
        """Gets the text of an element."""
        return self.driver.get_text(locator, timeout)


class MainPage(BasePage):
    """Main Page"""
    
    # Element Locators
    SEARCH_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/search_button")
    LOCATION_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/location_button")
    MENU_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/menu_button")
    CURRENT_TEMPERATURE = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/current_temperature")
    WEATHER_DESCRIPTION = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/weather_description")
    HUMIDITY_TEXT = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/humidity_text")
    WIND_SPEED_TEXT = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/wind_speed_text")
    
    def click_search(self):
        """Clicks the search button."""
        self.click_element(self.SEARCH_BUTTON)
    
    def click_location(self):
        """Clicks the location button."""
        self.click_element(self.LOCATION_BUTTON)
    
    def click_menu(self):
        """Clicks the menu button."""
        self.click_element(self.MENU_BUTTON)
    
    def get_current_temperature(self):
        """Gets the current temperature."""
        temp_text = self.get_text(self.CURRENT_TEMPERATURE)
        # Extract the numeric part
        import re
        temp_match = re.search(r'(\d+)', temp_text)
        return int(temp_match.group(1)) if temp_match else None
    
    def get_weather_description(self):
        """Gets the weather description."""
        return self.get_text(self.WEATHER_DESCRIPTION)
    
    def get_humidity(self):
        """Gets the humidity."""
        humidity_text = self.get_text(self.HUMIDITY_TEXT)
        import re
        humidity_match = re.search(r'(\d+)', humidity_text)
        return int(humidity_match.group(1)) if humidity_match else None
    
    def get_wind_speed(self):
        """Gets the wind speed."""
        wind_text = self.get_text(self.WIND_SPEED_TEXT)
        import re
        wind_match = re.search(r'(\d+)', wind_text)
        return int(wind_match.group(1)) if wind_match else None


class SearchPage(BasePage):
    """Search Page"""
    
    # Element Locators
    SEARCH_INPUT = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/search_input")
    SEARCH_RESULTS = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/search_results")
    CITY_ITEM = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/city_item")
    BACK_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/back_button")
    
    def search_city(self, city_name):
        """Searches for a city."""
        self.input_text(self.SEARCH_INPUT, city_name)
    
    def select_city(self, city_name):
        """Selects a city."""
        # This needs to locate the element based on the actual city name
        city_locator = (AppiumBy.XPATH, f"//android.widget.TextView[@text='{city_name}']")
        self.click_element(city_locator)
    
    def click_back(self):
        """Clicks the back button."""
        self.click_element(self.BACK_BUTTON)


class MenuPage(BasePage):
    """Menu Page"""
    
    # Element Locators
    SETTINGS_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/settings_button")
    ABOUT_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/about_button")
    HELP_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/help_button")
    CLOSE_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/close_button")
    
    def click_settings(self):
        """Clicks the settings button."""
        self.click_element(self.SETTINGS_BUTTON)
    
    def click_about(self):
        """Clicks the about button."""
        self.click_element(self.ABOUT_BUTTON)
    
    def click_help(self):
        """Clicks the help button."""
        self.click_element(self.HELP_BUTTON)
    
    def click_close(self):
        """Clicks the close button."""
        self.click_element(self.CLOSE_BUTTON)


class SettingsPage(BasePage):
    """Settings Page"""
    
    # Element Locators
    TEMPERATURE_UNIT_TOGGLE = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/temperature_unit_toggle")
    NOTIFICATION_TOGGLE = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/notification_toggle")
    AUTO_REFRESH_TOGGLE = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/auto_refresh_toggle")
    LANGUAGE_SELECTOR = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/language_selector")
    
    def toggle_temperature_unit(self):
        """Toggles the temperature unit."""
        self.click_element(self.TEMPERATURE_UNIT_TOGGLE)
    
    def toggle_notification(self):
        """Toggles the notification setting."""
        self.click_element(self.NOTIFICATION_TOGGLE)
    
    def toggle_auto_refresh(self):
        """Toggles auto-refresh."""
        self.click_element(self.AUTO_REFRESH_TOGGLE)
    
    def select_language(self, language):
        """Selects a language."""
        self.click_element(self.LANGUAGE_SELECTOR)
        language_locator = (AppiumBy.XPATH, f"//android.widget.TextView[@text='{language}']")
        self.click_element(language_locator) 