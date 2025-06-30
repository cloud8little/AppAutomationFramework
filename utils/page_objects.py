"""
我的天文台应用页面对象模型
"""
from appium.webdriver.common.appiumby import AppiumBy
from utils.app_driver import AppDriver


class BasePage:
    """基础页面类"""
    
    def __init__(self, driver: AppDriver):
        self.driver = driver
    
    def wait_for_element(self, locator, timeout=None):
        """等待元素出现"""
        return self.driver.find_element(locator, timeout)
    
    def click_element(self, locator, timeout=None):
        """点击元素"""
        self.driver.click_element(locator, timeout)
    
    def input_text(self, locator, text, timeout=None):
        """输入文本"""
        self.driver.input_text(locator, text, timeout)
    
    def get_text(self, locator, timeout=None):
        """获取元素文本"""
        return self.driver.get_text(locator, timeout)


class MainPage(BasePage):
    """主页面"""
    
    # 元素定位器
    SEARCH_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/search_button")
    LOCATION_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/location_button")
    MENU_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/menu_button")
    CURRENT_TEMPERATURE = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/current_temperature")
    WEATHER_DESCRIPTION = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/weather_description")
    HUMIDITY_TEXT = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/humidity_text")
    WIND_SPEED_TEXT = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/wind_speed_text")
    
    def click_search(self):
        """点击搜索按钮"""
        self.click_element(self.SEARCH_BUTTON)
    
    def click_location(self):
        """点击定位按钮"""
        self.click_element(self.LOCATION_BUTTON)
    
    def click_menu(self):
        """点击菜单按钮"""
        self.click_element(self.MENU_BUTTON)
    
    def get_current_temperature(self):
        """获取当前温度"""
        temp_text = self.get_text(self.CURRENT_TEMPERATURE)
        # 提取数字部分
        import re
        temp_match = re.search(r'(\d+)', temp_text)
        return int(temp_match.group(1)) if temp_match else None
    
    def get_weather_description(self):
        """获取天气描述"""
        return self.get_text(self.WEATHER_DESCRIPTION)
    
    def get_humidity(self):
        """获取湿度"""
        humidity_text = self.get_text(self.HUMIDITY_TEXT)
        import re
        humidity_match = re.search(r'(\d+)', humidity_text)
        return int(humidity_match.group(1)) if humidity_match else None
    
    def get_wind_speed(self):
        """获取风速"""
        wind_text = self.get_text(self.WIND_SPEED_TEXT)
        import re
        wind_match = re.search(r'(\d+)', wind_text)
        return int(wind_match.group(1)) if wind_match else None


class SearchPage(BasePage):
    """搜索页面"""
    
    # 元素定位器
    SEARCH_INPUT = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/search_input")
    SEARCH_RESULTS = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/search_results")
    CITY_ITEM = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/city_item")
    BACK_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/back_button")
    
    def search_city(self, city_name):
        """搜索城市"""
        self.input_text(self.SEARCH_INPUT, city_name)
    
    def select_city(self, city_name):
        """选择城市"""
        # 这里需要根据实际的城市名称来定位元素
        city_locator = (AppiumBy.XPATH, f"//android.widget.TextView[@text='{city_name}']")
        self.click_element(city_locator)
    
    def click_back(self):
        """点击返回按钮"""
        self.click_element(self.BACK_BUTTON)


class MenuPage(BasePage):
    """菜单页面"""
    
    # 元素定位器
    SETTINGS_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/settings_button")
    ABOUT_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/about_button")
    HELP_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/help_button")
    CLOSE_BUTTON = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/close_button")
    
    def click_settings(self):
        """点击设置按钮"""
        self.click_element(self.SETTINGS_BUTTON)
    
    def click_about(self):
        """点击关于按钮"""
        self.click_element(self.ABOUT_BUTTON)
    
    def click_help(self):
        """点击帮助按钮"""
        self.click_element(self.HELP_BUTTON)
    
    def click_close(self):
        """点击关闭按钮"""
        self.click_element(self.CLOSE_BUTTON)


class SettingsPage(BasePage):
    """设置页面"""
    
    # 元素定位器
    TEMPERATURE_UNIT_TOGGLE = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/temperature_unit_toggle")
    NOTIFICATION_TOGGLE = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/notification_toggle")
    AUTO_REFRESH_TOGGLE = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/auto_refresh_toggle")
    LANGUAGE_SELECTOR = (AppiumBy.ID, "com.weather.forecast.weatherlive:id/language_selector")
    
    def toggle_temperature_unit(self):
        """切换温度单位"""
        self.click_element(self.TEMPERATURE_UNIT_TOGGLE)
    
    def toggle_notification(self):
        """切换通知设置"""
        self.click_element(self.NOTIFICATION_TOGGLE)
    
    def toggle_auto_refresh(self):
        """切换自动刷新"""
        self.click_element(self.AUTO_REFRESH_TOGGLE)
    
    def select_language(self, language):
        """选择语言"""
        self.click_element(self.LANGUAGE_SELECTOR)
        language_locator = (AppiumBy.XPATH, f"//android.widget.TextView[@text='{language}']")
        self.click_element(language_locator) 