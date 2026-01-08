import Utils.Locators as loc
import Utils.Data as data
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import base64
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException as exceptions
import time


class RegistryPage:
    def __init__(self, driver):
        self.driver = driver

    def GlobalSearch (self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, loc.globalsearchbar_id)))
            self.driver.find_element(By.ID, loc.globalsearchbar_id).send_keys(data.patient_cz_id)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, loc.searchresult_id)))
            self.driver.find_element(By.ID, loc.searchresult_id).find_elements(By.TAG_NAME, "li")[1].click()
            print("Global Search Successful")
            self.driver.switch_to.window(self.driver.window_handles[1])
        except exceptions as e:
            print("Global Search Failed: ", e)