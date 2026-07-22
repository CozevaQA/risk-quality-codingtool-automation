import json

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.RiskPOC import Risk_POC
from utils import web_utils as webfunctions
from pages.BasePage import BasePage
from pages.locators.PatientDashboardLocators import PatientDashboardLocators


class Patient_Dashboard(BasePage):

    def __init__(self, driver, timeout, cozeva_id):
        super().__init__(driver, timeout)
        self.cozeva_id = cozeva_id


    def open_patient_dashboard(self, baseurl):
        base = baseurl

        endpoint = (
            f"/patient_detail/{self.cozeva_id}?tab_type=CareOps&session=YXBwX2lkPXJlZ2lzdHJpZXMmY3VzdElkPTE1MDAmZG9jdG9yc1BlcnNvbklkPTk2MjgzMzYmZG9jdG9yX3VpZD05NjA4MjQ3JnBheWVySWQ9MTUwMCZwVWlkPTUzNDQ1JnF1YXJ0ZXI9MjAyNS0xMi0zMSZob21lPVlYQndYMmxrUFhKbFoybHpkSEpwWlhNbVkzVnpkRWxrUFRFMU1EQW1jR0Y1WlhKSlpEMHhOVEF3Sm05eVowbGtQVEUxTURBJmZpbHRlcl9vcmdfaWQ9MTUwMA%3D%3D&first_load=1"
        )

        url = base + endpoint
        print("url created:", url)

        try:
            print("Loading Patient Dashboard")
            self.driver.get(url)

            webfunctions.wait_for_page_load(self.driver, 120)

            WebDriverWait(self.driver, 120).until(
                EC.visibility_of_element_located(PatientDashboardLocators.HCC_TABLE)
            )
            if len(self.driver.find_elements(*PatientDashboardLocators.HIDE_BANNER)) > 0:
                webfunctions.action_click(self.driver, self.driver.find_element(*PatientDashboardLocators.HIDE_BANNER))
            return True

        except Exception as e:
            print("Failed to load patient dashboard:", e)
            return False


    def get_stale_hccs(self):
        stale_hccs = []
        stale_measures=self.driver.find_elements(*PatientDashboardLocators.STALE_HCC_MEASURES)
        for stale_measure in stale_measures:
            hcc_info_str = stale_measure.get_attribute("data-hcc_info")
            hcc_info = json.loads(hcc_info_str)
            hcc_id = hcc_info["hcc_id"]
            stale_hccs.append(hcc_id)
        print("Stale HCCS")
        return stale_hccs

    def get_hollow_dot_hccs(self):
        hollow_dot_hccs = []
        hollow_dot_measures = self.driver.find_elements(*PatientDashboardLocators.HOLLOW_DOT_HCCS)
        for hollow_dot_measure in hollow_dot_measures:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                hollow_dot_measure
            )
            hcc_info_str = hollow_dot_measure.get_attribute("data-hcc_info")
            hcc_info = json.loads(hcc_info_str)
            hcc_id = hcc_info["hcc_id"]
            hollow_dot_hccs.append(hcc_id)
        print("Hollow dot hccs ", hollow_dot_hccs)
        return hollow_dot_hccs

    def get_no_dot_hccs(self):
        no_dot_hccs = []
        no_dot_measures = self.driver.find_elements(*PatientDashboardLocators.NO_DOT_HCCS)
        for no_dot_measure in no_dot_measures:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                no_dot_measure
            )
            hcc_info_str = no_dot_measure.get_attribute("data-hcc_info")
            hcc_info = json.loads(hcc_info_str)
            hcc_id = hcc_info["hcc_id"]
            no_dot_hccs.append(hcc_id)
        print("No dot hccs ", no_dot_hccs)
        return no_dot_hccs





    def get_non_compliant_dx(self):
        non_compliant_dx = []

        dx_code_elements = self.driver.find_elements(
            *PatientDashboardLocators.NON_COMPLIANT_DX
        )

        for element in dx_code_elements:
            non_compliant_dx.append(element.get_attribute("id"))

        print(f"List of DX {non_compliant_dx}")
        return non_compliant_dx

    def get_risk_gaps(self):
        red_dots = self.driver.find_elements(*PatientDashboardLocators.HCC_RED_DOTS)
        return len(red_dots)

    def get_stale_dx_hcc(self):
        """
        Collects DX codes mapped to stale HCCs from the Patient Dashboard.

        Returns:
            List of lists in the format:
            [
                [dx_code_1, hcc_id],
                [dx_code_2, hcc_id],
                ...
            ]
        """

        # Find all HCC rows on the dashboard
        hcc_rows = self.driver.find_elements(*PatientDashboardLocators.HCC_ROW)

        # Final processed output
        processed_dx_hcc = []

        # Iterate through each HCC row
        for hcc_row in hcc_rows:

            # Extract HCC info from data attribute
            hcc_id = None
            hcc_info_raw = hcc_row.get_attribute("data-hcc_info")

            if hcc_info_raw:
                hcc_info = json.loads(hcc_info_raw)
                hcc_id = hcc_info.get("hcc_id")

            # Check if this HCC row has a STALE icon
            try:
                hcc_row.find_element(*PatientDashboardLocators.STALE_ICON)
                is_stale = True
            except NoSuchElementException:
                is_stale = False

            # Only process stale HCCs
            if not is_stale:
                continue

            # Find all DX codes under this HCC
            dx_codes = hcc_row.find_elements(*PatientDashboardLocators.DX_CODES_HCC)

            for dx_code in dx_codes:
                dx_id = dx_code.get_attribute("id").replace(".","")

                if dx_id and hcc_id is not None:
                    # Append DX–HCC mapping as a list
                    processed_dx_hcc.append([dx_id, hcc_id])

        return processed_dx_hcc


    def open_poc(self):
        # Click pencil icon
        pencil_icon = self.driver.find_element(
            *PatientDashboardLocators.FIRST_PENCIL_ICON
        )
        webfunctions.action_click(self.driver, pencil_icon)

        try:
            print("Looking for Confirm/Disconfirm button...")

            open_poc_button = self.driver.find_element(
                *PatientDashboardLocators.OPEN_POC_BUTTON
            )
            print("open_poc_button FOUND")

            print("Clicking Confirm/Disconfirm...")
            webfunctions.action_click(self.driver, open_poc_button)
            print("Clicked. Waiting for page load...")

            return Risk_POC(self.driver, self.timeout)

        except Exception as e:
            print("open_poc failed because:", e)
            raise e

    def get_document_list(self):
        """
        Navigates to Documents section and returns list of documents.
        Page layer does NOT assert.

        Returns:
            List[str] → document names
        """
        documents_list = []

        try:
            # Ensure page is loaded
            webfunctions.wait_for_page_load(self.driver, 120)

            # Click first dropdown
            first_dropdown = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(PatientDashboardLocators.FIRST_DROPDOWN_XPATH)
            )
            webfunctions.action_click(self.driver, first_dropdown)

            # Click second dropdown
            second_dropdown = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(PatientDashboardLocators.SECOND_DROPDOWN_XPATH)
            )
            webfunctions.action_click(self.driver, second_dropdown)

            # Click Documents link
            documents_link = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(PatientDashboardLocators.DOCUMENTS_LINK)
            )
            webfunctions.action_click(self.driver, documents_link)

            # Wait for documents page to load
            webfunctions.wait_for_page_load(self.driver, 120)

            # Collect documents
            document_elements = self.driver.find_elements(
                *PatientDashboardLocators.DOCUMENTS
            )

            for doc in document_elements:
                doc_text = doc.text.strip()
                if doc_text:
                    documents_list.append(doc_text)

            # print(f"[get_document_list] Found documents: {documents_list}")

            return documents_list

        except Exception as e:
            print(f"[get_document_list][ERROR] Failed to fetch documents: {e}")
            return documents_list

    def get_dot_status_by_hcc_id(self, hcc_id):
        """
        Returns previous dot status for a given HCC ID.

        Args:
            hcc_id (str | int)

        Returns:
            str | None: prev_status value if present, else None
        """
        try:
            hcc_row_xpath = (
                f"//*[contains(@class,'hcc_row') and "
                f"contains(@data-hcc_info, '{hcc_id}')]"
            )

            hcc_row = self.driver.find_element(By.XPATH, hcc_row_xpath)

            # get_attribute returns None if attribute does not exist
            prev_status = hcc_row.get_attribute("prev_status")

            if prev_status:
                return prev_status.strip()

            return None

        except NoSuchElementException:
            return None

    def get_dot_status_by_dx(self, dx_code):
        """
        Returns dot status for a given DX code.

        Args:
            dx_code (str): DX code (e.g., I8500, I85.00)

        Returns:
            str | None: prev_status if present, else None
        """
        try:
            # Normalize DX code matching (ignore dots)
            dx_code_xpath = (
                f"//*[contains("
                f"translate(normalize-space(text()), '.', ''),"
                f"'{dx_code}'"
                f")]"
            )

            dx_element = self.driver.find_element(By.XPATH, dx_code_xpath)

        except NoSuchElementException:
            # DX not found on page
            return None

        try:
            # Find parent HCC row relative to DX
            hcc_row = dx_element.find_element(
                By.XPATH,
                "ancestor::div[contains(@class,'clear hcc_row')]"
            )
            # print(hcc_row.get_attribute("id"))
        except NoSuchElementException:
            # DX found but HCC row not resolved
            return None

        try:
            # Find dot status element
            dot_element = hcc_row.find_element(
                *PatientDashboardLocators.HCC_DOT_STATUS
            )

            prev_status = dot_element.get_attribute("prev_status")
            # print(prev_status
            #       )
            return prev_status.strip() if prev_status else None

        except NoSuchElementException:
            # Dot status element not present
            return None