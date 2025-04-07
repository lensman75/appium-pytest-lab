import pytest
import time
import json
import argparse
import os
from appium import webdriver
from appium. options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

json_path = r"json\card.json"

# parser = argparse.ArgumentParser()
# parser.add_argument("--hotel", type=str)
# parser.add_argument("--day", type=int)
# parser.add_argument("--date", type=str)
# args = parser.parse_args()

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
    # url = 'http://10.255.255.254:4723/wd/hub'
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
    sleep_duration = 7
    # target_day = "13"
    target_day = os.getenv("DAY")
    
    # target_date = "June 2025"
    target_date = os.getenv("DATE")
    ENTER_KEY_CODE = 66
    # target_hotel = "The Chester Grosvenor" # The Chester Grosvenor selected as second iteration, because no results for The Grosvenor Hotel
    target_hotel = os.getenv("HOTEL")
    print(target_day, target_date, target_hotel)
    seach_hotel = "The Grosvenor Hotel"

    print("Test started")
    element = appium_driver.find_element(AppiumBy.ID, "com.tripadvisor.tripadvisor:id/bdlBtnSkip")
    element.click()
    time.sleep(sleep_duration)
    tabsearch = appium_driver.find_element(AppiumBy.ID, "com.tripadvisor.tripadvisor:id/tab_search")
    tabsearch.click()
    time.sleep(sleep_duration)
    search_field = appium_driver.find_element(AppiumBy.ID, "com.tripadvisor.tripadvisor:id/edtSearchString")
    # search_field.send_keys(seach_hotel)
    search_field.send_keys(target_hotel)
    appium_driver.press_keycode(ENTER_KEY_CODE)
    time.sleep(sleep_duration)
    element_hotels = appium_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Hotels")')
    element_hotels.click()
    time.sleep(sleep_duration)

    # Looking for elements that contain hotel names
    hotel_elements = appium_driver.find_elements(AppiumBy.XPATH, "//android.widget.TextView[@content-desc]")
    time.sleep(sleep_duration)
    
    time.sleep(sleep_duration)
    hotel_names = [element.get_attribute("content-desc").rstrip(". ") for element in hotel_elements]
    time.sleep(sleep_duration)
    print(hotel_names)
    if target_hotel in hotel_names:
        print(f"Found hotel: {target_hotel}")
        target_index = hotel_names.index(target_hotel)
        hotel_elements[target_index].click()
        time.sleep(sleep_duration)
        
        try:
            # Using UiScrollable for scrilling to that date
            element = appium_driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true))'
                f'.scrollIntoView(new UiSelector().resourceId("com.tripadvisor.tripadvisor:id/txtTitle").text("{target_date}"))'
            )
            # element.click()
            time.sleep(sleep_duration)
            print(f"Date found: {target_date}")
        except NoSuchElementException:
            print(f"Not found date: {target_date}")
        
        try:
            # Search for day
            element = appium_driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().resourceId("com.tripadvisor.tripadvisor:id/txtDay").text("{target_day}")'
            )
            element.click()
            time.sleep(sleep_duration)
            print(f"Day {target_day} selected.")
        except NoSuchElementException:
            print(f"Day {target_day} not found.")
        try:
            # Search buttons
            element = appium_driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().resourceId("com.tripadvisor.tripadvisor:id/btnPrimary")'
            )
            element.click()
            time.sleep(sleep_duration)
            print("Button pressed.")
        except NoSuchElementException:
            print("Not found button.")
        try:
            element = appium_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.tripadvisor.tripadvisor:id/btnAllDeals")'
            )
            element.click()
            time.sleep(sleep_duration)
            print("Button pressed.")
        except NoSuchElementException:
            print("Not found button.")
        
        #Provider and prices
        cards = appium_driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.tripadvisor.tripadvisor:id/cardHotelOffer")')
        if not cards:
            print("No cards found")
        else:
            print(f"Found {len(cards)} cards.\n")
        # resp_dict = {}
        for i, card in enumerate(cards):
            try:
                provider = card.find_element(
                    AppiumBy.ID,
                    "com.tripadvisor.tripadvisor:id/imgProviderLogo"
                ).get_attribute("content-desc")
            except:
                provider = "Provider not found"

            try:
                price = card.find_element(
                    AppiumBy.ID,
                    "com.tripadvisor.tripadvisor:id/txtPriceTopDeal"
                ).text
            except:
                price = "Price not found"

            print(f"Card: {i + 1}:")
            print(f"Provider{i}: {provider}")
            print(f"Price: {price}")



            if os.path.exists(json_path):
                with open(json_path, "r") as infile:
                    try:
                        resp_dict = json.load(infile)
                    except json.JSONDecodeError:
                        resp_dict = {}
            else:
                resp_dict = {}

            if target_hotel not in resp_dict:
                resp_dict[target_hotel] = {}

            resp_dict[target_hotel][f"{target_date}-{target_day}"] = {
                provider: price
            }

            with open(json_path, "w") as outfile:
                json.dump(resp_dict, outfile, indent=4)




    else:
        print(f"No such hotel: {target_hotel}")

    print("Test finished")
    time.sleep(sleep_duration)
    # TODO(lensman75): Make crossplatform
    appium_driver.get_screenshot_as_file(r"screenshots\screenshot.png")
    # time.sleep(sleep_duration)
    # input("Press Enter, to exit...")
