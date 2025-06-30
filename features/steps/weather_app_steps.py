"""
我的天文台应用测试步骤实现
"""
from behave import given, when, then, step
from utils.app_driver import AppDriver
from utils.test_data_manager import TestDataManager
from utils.page_objects import MainPage, SearchPage, MenuPage, SettingsPage
import time


@given('我打开了我的天文台应用')
def step_open_weather_app(context):
    """打开我的天文台应用"""
    context.driver = AppDriver(platform="android")
    context.driver.start_driver()
    context.main_page = MainPage(context.driver)
    context.test_data = TestDataManager()
    
    # 等待应用加载完成
    time.sleep(3)


@given('我在主页面')
def step_on_main_page(context):
    """确认在主页面"""
    # 检查主页面元素是否存在
    assert context.driver.is_element_present(context.main_page.SEARCH_BUTTON), "搜索按钮未找到"


@when('我点击搜索按钮')
def step_click_search_button(context):
    """点击搜索按钮"""
    context.main_page.click_search()
    context.search_page = SearchPage(context.driver)
    time.sleep(2)


@when('我搜索城市 "{city_name}"')
def step_search_city(context, city_name):
    """搜索指定城市"""
    context.search_page.search_city(city_name)
    time.sleep(2)


@when('我选择城市 "{city_name}"')
def step_select_city(context, city_name):
    """选择指定城市"""
    context.search_page.select_city(city_name)
    time.sleep(2)


@when('我点击定位按钮')
def step_click_location_button(context):
    """点击定位按钮"""
    context.main_page.click_location()
    time.sleep(3)


@when('我点击菜单按钮')
def step_click_menu_button(context):
    """点击菜单按钮"""
    context.main_page.click_menu()
    context.menu_page = MenuPage(context.driver)
    time.sleep(2)


@when('我点击设置按钮')
def step_click_settings_button(context):
    """点击设置按钮"""
    context.menu_page.click_settings()
    context.settings_page = SettingsPage(context.driver)
    time.sleep(2)


@when('我切换温度单位')
def step_toggle_temperature_unit(context):
    """切换温度单位"""
    context.settings_page.toggle_temperature_unit()
    time.sleep(1)


@when('我切换通知设置')
def step_toggle_notification(context):
    """切换通知设置"""
    context.settings_page.toggle_notification()
    time.sleep(1)


@then('我应该看到当前温度信息')
def step_see_current_temperature(context):
    """验证当前温度信息显示"""
    temperature = context.main_page.get_current_temperature()
    assert temperature is not None, "未找到温度信息"
    assert context.test_data.validate_temperature(temperature), f"温度值 {temperature} 不在合理范围内"


@then('我应该看到天气描述')
def step_see_weather_description(context):
    """验证天气描述显示"""
    description = context.main_page.get_weather_description()
    assert description, "未找到天气描述"
    assert len(description) > 0, "天气描述为空"


@then('我应该看到湿度信息')
def step_see_humidity_info(context):
    """验证湿度信息显示"""
    humidity = context.main_page.get_humidity()
    assert humidity is not None, "未找到湿度信息"
    assert context.test_data.validate_humidity(humidity), f"湿度值 {humidity} 不在合理范围内"


@then('我应该看到风速信息')
def step_see_wind_speed_info(context):
    """验证风速信息显示"""
    wind_speed = context.main_page.get_wind_speed()
    assert wind_speed is not None, "未找到风速信息"
    wind_range = context.test_data.get_expected_weather_range().get("wind_speed_range", {})
    min_wind = wind_range.get("min", 0)
    max_wind = wind_range.get("max", 100)
    assert min_wind <= wind_speed <= max_wind, f"风速值 {wind_speed} 不在合理范围内"


@then('搜索页面应该显示')
def step_search_page_should_display(context):
    """验证搜索页面显示"""
    assert context.driver.is_element_present(context.search_page.SEARCH_INPUT), "搜索输入框未找到"


@then('城市 "{city_name}" 应该被选中')
def step_city_should_be_selected(context, city_name):
    """验证城市被选中"""
    # 这里可以检查页面标题或其他标识来确认城市已选中
    time.sleep(2)
    # 可以根据实际应用的元素来验证


@then('设置页面应该显示')
def step_settings_page_should_display(context):
    """验证设置页面显示"""
    assert context.driver.is_element_present(context.settings_page.TEMPERATURE_UNIT_TOGGLE), "温度单位切换按钮未找到"


@step('我关闭应用')
def step_close_app(context):
    """关闭应用"""
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit_driver()


# 数据驱动测试步骤
@given('我使用测试数据中的城市 "{city_key}"')
def step_use_test_city(context, city_key):
    """使用测试数据中的城市"""
    context.city_data = context.test_data.get_city_data(city_key)
    context.city_name = context.test_data.get_city_name(city_key)
    assert context.city_name, f"未找到城市数据: {city_key}"


@then('温度应该在合理范围内')
def step_temperature_should_be_reasonable(context):
    """验证温度在合理范围内"""
    temperature = context.main_page.get_current_temperature()
    assert context.test_data.validate_temperature(temperature), f"温度 {temperature} 不在合理范围内"


@then('湿度应该在合理范围内')
def step_humidity_should_be_reasonable(context):
    """验证湿度在合理范围内"""
    humidity = context.main_page.get_humidity()
    assert context.test_data.validate_humidity(humidity), f"湿度 {humidity} 不在合理范围内" 