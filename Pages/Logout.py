import Utils.Locators as loc
import Utils.Data as data
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import base64
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException as exceptions
import time


class LogoutPage:
    def __init__(self, driver):
        self.driver = driver

    def logout (self):
        try:
            self.driver.find_element(By.XPATH, loc.user_icon_xpath).click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, loc.logout_btn_xpath).click()
            time.sleep(1)
            print("Logout Successful")
        except exceptions as e:
            print("Logout Failed: ", e)
