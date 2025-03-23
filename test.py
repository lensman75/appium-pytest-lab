import pytest
import time
from appium import webdriver
from appium. options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

def initialize_appium_driver():
    desired_caps = {
        "appium:platformName": "Android",
        "appium:platformVersion": "9",
        "appium:deviceName": "988a9b304a3834575830",
        "appium:appPackage": "com.tripadvisor.tripadvisor",
        "appium:automationName": "UIAutomator2",
        "appium:ensureWebViewsHavePages": "true",
        "appium:appActivity": "com.tripadvisor.tripadvisor/com.tripadvisor.android.ui.launcher.LauncherActivity"
    }

    url = 'http://localhost:4723'
    driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(desired_caps))
    return driver

@pytest.fixture(scope="function")
def appium_driver(request):
    driver = initialize_appium_driver()

    def fin():
        driver.quit()

    request.addfinalizer(fin)
    return driver

def test_example(appium_driver):
    print("Test started")
    element = appium_driver.find_element(AppiumBy.ID, "com.tripadvisor.tripadvisor:id/bdlBtnSkip")
    element.click()
    tabsearch = appium_driver.find_element(AppiumBy.ID, "com.tripadvisor.tripadvisor:id/tab_search")
    tabsearch.click()
    search_field = appium_driver.find_element(AppiumBy.ID, "com.tripadvisor.tripadvisor:id/edtSearchString")
    search_field.send_keys("The Grosvenor Hotel")
    appium_driver.press_keycode(66)
    element_hotels = appium_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Hotels")')
    element_hotels.click()
