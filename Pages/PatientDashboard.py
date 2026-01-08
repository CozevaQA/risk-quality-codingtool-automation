import Utils.Locators as loc
import Utils.Data as data
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import base64
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException as exceptions
import time

class PatientDashboardPage:
    def __init__(self, driver):
        self.driver = driver

    def ajax_preloader_wait(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "ajax_preloader")))
        except exceptions as e:
            print("Ajax Preloader wait failed: ", e)

    def OpenPOC (self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.dasboard_xpath)))
            self.driver.find_element(By.XPATH, loc.pencil_icon_xpath).click()
            time.sleep(1)
            self.driver.find_elements(By.XPATH, loc.confirm_disconfirm_xpath)[1].click()
            self.ajax_preloader_wait()
            print("POC Opened Successfully")
        except exceptions as e:
            print("POC Opening Failed: ", e)

    def OpenPreReview (self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.dasboard_xpath)))
            self.driver.find_element(By.XPATH, loc.pencil_icon_xpath).click()
            time.sleep(1)
            self.driver.find_elements(By.XPATH, loc.confirm_disconfirm_xpath)[1].click()
            self.ajax_preloader_wait()
            print("Pre-Review Opened Successfully")
        except exceptions as e:
            print("Pre-Review Opening Failed: ", e)

    def OpenQualityCodingTool (self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.dasboard_xpath)))
            self.driver.find_element(By.XPATH, loc.pencil_icon_xpath).click()
            self.ajax_preloader_wait()
            print("Quality Coding Tool Opened Successfully")
        except exceptions as e:
            print("Quality Coding Tool Opening Failed: ", e)

