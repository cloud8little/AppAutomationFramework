"""
APP自动化测试驱动管理类
"""
import yaml
import os
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class AppDriver:
    """APP驱动管理类"""
    
    def __init__(self, platform="android"):
        """
        初始化APP驱动
        
        Args:
            platform (str): 平台类型，支持 "android" 或 "ios"
        """
        self.platform = platform
        self.driver = None
        self.config = self._load_config()
        
    def _load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    def start_driver(self):
        """启动APP驱动"""
        try:
            # 获取平台配置
            platform_config = self.config['environments'][self.platform]
            appium_config = self.config['appium']
            
            # 构建Appium服务器URL
            server_url = f"http://{appium_config['host']}:{appium_config['port']}{appium_config['path']}"
            
            # 创建驱动
            self.driver = webdriver.Remote(server_url, platform_config)
            
            # 设置隐式等待
            self.driver.implicitly_wait(self.config['test_data']['implicit_wait'])
            
            print(f"成功启动 {self.platform} 平台驱动")
            return self.driver
            
        except Exception as e:
            print(f"启动驱动失败: {str(e)}")
            raise
    
    def quit_driver(self):
        """退出驱动"""
        if self.driver:
            self.driver.quit()
            print("驱动已退出")
    
    def find_element(self, locator, timeout=None):
        """
        查找元素
        
        Args:
            locator (tuple): 元素定位器 (By, value)
            timeout (int): 超时时间
            
        Returns:
            WebElement: 找到的元素
        """
        if timeout is None:
            timeout = self.config['test_data']['default_timeout']
            
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            print(f"元素未找到: {locator}")
            raise
    
    def click_element(self, locator, timeout=None):
        """点击元素"""
        element = self.find_element(locator, timeout)
        element.click()
    
    def input_text(self, locator, text, timeout=None):
        """输入文本"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=None):
        """获取元素文本"""
        element = self.find_element(locator, timeout)
        return element.text
    
    def is_element_present(self, locator, timeout=None):
        """检查元素是否存在"""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def take_screenshot(self, filename):
        """截图"""
        if self.driver:
            screenshot_path = os.path.join(
                os.path.dirname(__file__), "..", "screenshots", filename
            )
            self.driver.save_screenshot(screenshot_path)
            print(f"截图已保存: {screenshot_path}")
            return screenshot_path 