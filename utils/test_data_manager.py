"""
Test Data Management Class.
"""
import yaml
import os
import json
from typing import Dict, Any


class TestDataManager:
    """Manages test data."""
    
    def __init__(self):
        """Initializes the Test Data Manager."""
        self.test_data_path = os.path.join(os.path.dirname(__file__), "..", "test_data")
        self._load_all_data()
    
    def _load_all_data(self):
        """Loads all test data from files."""
        self.weather_data = self._load_yaml_file("weather_data.yaml")
        self.cities = self.weather_data.get("cities", {})
        self.weather_types = self.weather_data.get("weather_types", {})
        self.test_users = self.weather_data.get("test_users", {})
        self.expected_weather = self.weather_data.get("expected_weather", {})
    
    def _load_yaml_file(self, filename: str) -> Dict[str, Any]:
        """
        Loads a YAML file.
        
        Args:
            filename (str): The name of the file.
            
        Returns:
            Dict: The content of the file.
        """
        file_path = os.path.join(self.test_data_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"YAML file parsing error: {e}")
            return {}
    
    def get_city_data(self, city_key: str) -> Dict[str, Any]:
        """
        Gets data for a specific city.
        
        Args:
            city_key (str): The key for the city.
            
        Returns:
            Dict: The city's data.
        """
        return self.cities.get(city_key, {})
    
    def get_city_name(self, city_key: str) -> str:
        """Gets the name of a city."""
        city_data = self.get_city_data(city_key)
        return city_data.get("name", "")
    
    def get_city_coordinates(self, city_key: str) -> Dict[str, float]:
        """Gets the coordinates of a city."""
        city_data = self.get_city_data(city_key)
        return city_data.get("coordinates", {})
    
    def get_weather_type(self, weather_key: str) -> str:
        """Gets a weather type."""
        return self.weather_types.get(weather_key, "")
    
    def get_test_user(self, user_key: str) -> Dict[str, str]:
        """
        Gets data for a test user.
        
        Args:
            user_key (str): The key for the user.
            
        Returns:
            Dict: The user's data.
        """
        return self.test_users.get(user_key, {})
    
    def get_expected_weather_range(self) -> Dict[str, Dict[str, int]]:
        """Gets the expected weather range."""
        return self.expected_weather
    
    def validate_temperature(self, temperature: float) -> bool:
        """
        Validates if the temperature is within a reasonable range.
        
        Args:
            temperature (float): The temperature value.
            
        Returns:
            bool: True if within range, False otherwise.
        """
        temp_range = self.expected_weather.get("temperature_range", {})
        min_temp = temp_range.get("min", -50)
        max_temp = temp_range.get("max", 60)
        return min_temp <= temperature <= max_temp
    
    def validate_humidity(self, humidity: float) -> bool:
        """Validates if the humidity is within a reasonable range."""
        humidity_range = self.expected_weather.get("humidity_range", {})
        min_humidity = humidity_range.get("min", 0)
        max_humidity = humidity_range.get("max", 100)
        return min_humidity <= humidity <= max_humidity
    
    def get_all_cities(self) -> Dict[str, Dict[str, Any]]:
        """Gets all city data."""
        return self.cities
    
    def get_all_weather_types(self) -> Dict[str, str]:
        """Gets all weather types."""
        return self.weather_types 