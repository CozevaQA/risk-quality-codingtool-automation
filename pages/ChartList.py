import time

from selenium.common import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils import web_utils as webfunctions
from pages.BasePage import BasePage
from pages.locators.RiskPOCLocators import RiskPOCLocators
from pages.locators.RiskCodingToolLocators import RiskCodingToolLocators
import json

#
# class ChartList(BasePage):
#
#     def __init__(self, driver):
#         super().__init__(driver)
#
#
#     def get_added_(self,task_id):
#
#     def get_dos(self,task_id):
#
#     def get_provider(self,task_id):
#
#     def get_codes(self,task_id):
#
#     def get_conditions(self,task_id):
#
#     def get_attachment_icon(self,task_id):


