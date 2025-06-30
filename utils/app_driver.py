"""
Appium Driver Management Class for Automation Testing.
"""
import yaml
import os
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class AppDriver:
    """App Driver Management Class"""
    
    def __init__(self, platform="android"):
        """
        Initializes the App Driver.
        
        Args:
            platform (str): The target platform, supports "android" or "ios".
        """
        self.platform = platform
        self.driver = None
        self.config = self._load_config()
        
    def _load_config(self):
        """Loads the configuration file."""
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    def start_driver(self):
        """Starts the Appium driver."""
        try:
            # Get platform-specific configuration
            platform_config = self.config['environments'][self.platform]
            appium_config = self.config['appium']
            
            # Build the Appium server URL
            server_url = f"http://{appium_config['host']}:{appium_config['port']}{appium_config['path']}"
            
            # Create the driver instance
            self.driver = webdriver.Remote(server_url, platform_config)
            
            # Set implicit wait
            self.driver.implicitly_wait(self.config['test_data']['implicit_wait'])
            
            print(f"Successfully started driver for {self.platform} platform.")
            return self.driver
            
        except Exception as e:
            print(f"Failed to start driver: {str(e)}")
            raise
    
    def quit_driver(self):
        """Quits the driver."""
        if self.driver:
            self.driver.quit()
            print("Driver has been quit.")
    
    def find_element(self, locator, timeout=None):
        """
        Finds an element.
        
        Args:
            locator (tuple): Element locator (By, value).
            timeout (int): Timeout in seconds.
            
        Returns:
            WebElement: The found element.
        """
        if timeout is None:
            timeout = self.config['test_data']['default_timeout']
            
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            print(f"Element not found: {locator}")
            raise
    
    def click_element(self, locator, timeout=None):
        """Clicks an element."""
        element = self.find_element(locator, timeout)
        element.click()
    
    def input_text(self, locator, text, timeout=None):
        """Inputs text into an element."""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=None):
        """Gets the text of an element."""
        element = self.find_element(locator, timeout)
        return element.text
    
    def is_element_present(self, locator, timeout=None):
        """Checks if an element is present."""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def take_screenshot(self, filename):
        """Takes a screenshot."""
        if self.driver:
            screenshot_path = os.path.join(
                os.path.dirname(__file__), "..", "screenshots", filename
            )
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to: {screenshot_path}")
            return screenshot_path 