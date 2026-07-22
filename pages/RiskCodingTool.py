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
class RiskCodingTool(BasePage):

    def __init__(self, driver):
        super().__init__(driver)


    def delete_task(self, delete_reason):
        """
        Deletes a task by providing a delete reason.
        Page layer does NOT assert.
        """

        try:
            wait = WebDriverWait(self.driver, 15)

            # Step 1: Click Delete button
            delete_btn = wait.until(
                EC.element_to_be_clickable(RiskCodingToolLocators.DELETE_BUTTON)
            )
            webfunctions.action_click(self.driver, delete_btn)

            # Step 2: Enter delete reason
            delete_input = wait.until(
                EC.visibility_of_element_located(
                    RiskCodingToolLocators.DELETE_MODAL_INPUT
                )
            )
            delete_input.clear()
            delete_input.send_keys(delete_reason)

            # Step 3: Confirm delete
            confirm_btn = wait.until(
                EC.element_to_be_clickable(
                    RiskCodingToolLocators.DELETE_CONFIRM_BUTTON
                )
            )
            webfunctions.action_click(self.driver, confirm_btn)

            return {
                "deleted": True,
                "delete_reason": delete_reason
            }

        except Exception as e:
            return {
                "deleted": False,
                "delete_reason": delete_reason,
                "error": str(e)
            }

    # def get_notes(self):
    #
    # def get_added_codes(self):
    #
    # def get_encounter_info(self):

    def get_document_attached(self):
        try:
            print("Checking for document attached...")

            document_container = self.driver.find_element(
                *RiskCodingToolLocators.CHARTCONTAINER
            )

            document_name = self.driver.find_element(
                *RiskCodingToolLocators.DOCUMENT_NAME
            ).text

            return (document_name, document_container.is_displayed())

        except Exception:
            print("Document container not found")
            return ("", False)

    def get_dx_submitted(self):
        dx_codes = self.driver.find_elements(*RiskCodingToolLocators.ADDED_DX)

        dx_codes_list = [
            dx.get_attribute("old_val").replace(".", "")
            for dx in dx_codes
            if dx.get_attribute("old_val")
        ]

        return dx_codes_list

    def get_hcc_submitted(self):
        hcc_codes = self.driver.find_elements(*RiskCodingToolLocators.ADDED_HCCS)
        hcc_codes_list = [hcc_codes.text.replace("HCC ","") for hcc_codes in hcc_codes if hcc_codes.text != " "]
        return hcc_codes_list

    def get_encounter_info(self):
        try:
            number_of_encounters = len(
                self.driver.find_elements(*RiskCodingToolLocators.NUMBER_ENCOUNTERS)
            )

            providers = [
                provider.text
                for provider in self.driver.find_elements(*RiskCodingToolLocators.ENCOUNTER_PROVIDER)
            ]

            dates = [
                date.text
                for date in self.driver.find_elements(*RiskCodingToolLocators.ENCOUNTER_DATE)
            ]

            return number_of_encounters, providers, dates

        except Exception as e:
            print(f"Error getting encounter info: {e}")
            return 0, [], []

    def get_notes_info(self):
        try:
            notes_texts = []

            notes_icons = self.driver.find_elements(*RiskCodingToolLocators.NOTES_ICON)

            for icon in notes_icons:
                icon.click()

                # Optional wait if modal loads dynamically
                # WebDriverWait(self.driver, 10).until(
                #     EC.visibility_of_element_located(RiskCodingToolLocators.NOTES_TEXT)
                # )

                note_text = self.driver.find_element(
                    *RiskCodingToolLocators.NOTES_TEXT
                ).text

                notes_texts.append(note_text)

                # Close modal
                self.driver.find_element(
                    *RiskCodingToolLocators.NOTES_CLOSE_MODAL
                ).click()

            return len(notes_texts), notes_texts

        except Exception as e:
            print(f"Error getting notes info: {e}")
            return 0, []



