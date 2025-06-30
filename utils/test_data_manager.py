"""
测试数据管理类
"""
import yaml
import os
import json
from typing import Dict, Any


class TestDataManager:
    """测试数据管理类"""
    
    def __init__(self):
        """初始化测试数据管理器"""
        self.test_data_path = os.path.join(os.path.dirname(__file__), "..", "test_data")
        self._load_all_data()
    
    def _load_all_data(self):
        """加载所有测试数据"""
        self.weather_data = self._load_yaml_file("weather_data.yaml")
        self.cities = self.weather_data.get("cities", {})
        self.weather_types = self.weather_data.get("weather_types", {})
        self.test_users = self.weather_data.get("test_users", {})
        self.expected_weather = self.weather_data.get("expected_weather", {})
    
    def _load_yaml_file(self, filename: str) -> Dict[str, Any]:
        """
        加载YAML文件
        
        Args:
            filename (str): 文件名
            
        Returns:
            Dict: 文件内容
        """
        file_path = os.path.join(self.test_data_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"文件未找到: {file_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"YAML文件解析错误: {e}")
            return {}
    
    def get_city_data(self, city_key: str) -> Dict[str, Any]:
        """
        获取城市数据
        
        Args:
            city_key (str): 城市键名
            
        Returns:
            Dict: 城市数据
        """
        return self.cities.get(city_key, {})
    
    def get_city_name(self, city_key: str) -> str:
        """获取城市名称"""
        city_data = self.get_city_data(city_key)
        return city_data.get("name", "")
    
    def get_city_coordinates(self, city_key: str) -> Dict[str, float]:
        """获取城市坐标"""
        city_data = self.get_city_data(city_key)
        return city_data.get("coordinates", {})
    
    def get_weather_type(self, weather_key: str) -> str:
        """获取天气类型"""
        return self.weather_types.get(weather_key, "")
    
    def get_test_user(self, user_key: str) -> Dict[str, str]:
        """
        获取测试用户数据
        
        Args:
            user_key (str): 用户键名
            
        Returns:
            Dict: 用户数据
        """
        return self.test_users.get(user_key, {})
    
    def get_expected_weather_range(self) -> Dict[str, Dict[str, int]]:
        """获取预期天气范围"""
        return self.expected_weather
    
    def validate_temperature(self, temperature: float) -> bool:
        """
        验证温度是否在合理范围内
        
        Args:
            temperature (float): 温度值
            
        Returns:
            bool: 是否在范围内
        """
        temp_range = self.expected_weather.get("temperature_range", {})
        min_temp = temp_range.get("min", -50)
        max_temp = temp_range.get("max", 60)
        return min_temp <= temperature <= max_temp
    
    def validate_humidity(self, humidity: float) -> bool:
        """验证湿度是否在合理范围内"""
        humidity_range = self.expected_weather.get("humidity_range", {})
        min_humidity = humidity_range.get("min", 0)
        max_humidity = humidity_range.get("max", 100)
        return min_humidity <= humidity <= max_humidity
    
    def get_all_cities(self) -> Dict[str, Dict[str, Any]]:
        """获取所有城市数据"""
        return self.cities
    
    def get_all_weather_types(self) -> Dict[str, str]:
        """获取所有天气类型"""
        return self.weather_types 