import Utils.Locators as loc
import Utils.Data as data
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import base64
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException as exceptions


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login (self):
        try:
            username = data.username
            password = data.password
            LoginName = self.driver.find_element(By.ID, loc.uname_field_id)
            LoginName.send_keys(username)
            LoginPassword = self.driver.find_element(By.ID, loc.pwd_field_id)
            LoginPassword.send_keys(password)
            self.driver.find_element(By.ID, loc.submit_btn_id).click()
            WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.ID, loc.reason_field_id)))
            Reason = data.reason_field
            self.driver.find_element(By.ID, loc.reason_field_id).send_keys(Reason)
            self.driver.find_element(By.ID, loc.submit_btn_id).click()
            WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.ID, loc.payer_selector_id)))
            print("Login Successful")
        except exceptions as e:
            print("Login Failed: ", e)
            
    