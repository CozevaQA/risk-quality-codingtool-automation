import time

from selenium.common import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from utils import web_utils as webfunctions
from pages.BasePage import BasePage
from pages.locators.RiskPOCLocators import RiskPOCLocators
import json

class Risk_POC(BasePage):

    def is_page_loaded(self):
        """
        Waits for the submit button on the POC page to confirm it loaded.
        Returns self for chaining.
        """
        try:
            webfunctions.wait_for_page_load(self.driver)
            print("POC Page has loaded successfully")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.poc_body.poc_action_table")
                )
            )
            return self
        except TimeoutException:
            print("ERROR: POC page did not load within timeout")
            raise

    def visible_core_elements(self):
        checks = {
            "Service Year dropdown": self.is_visible_and_displayed(RiskPOCLocators.SERVICE_YEAR_DROPDOWN),
            "Add Dx button": self.is_visible_and_displayed(RiskPOCLocators.ADD_DX_BUTTON),
            "All HCCs toggle(default off)": (self.is_visible_and_displayed(RiskPOCLocators.ALL_HCCS_TOGGLE) and self.is_visible_and_displayed(RiskPOCLocators.ALL_HCCS_LABEL)),
            "Quality button": self.is_visible_and_displayed(RiskPOCLocators.QUALITY_BUTTON),
            "Add CPT link": self.is_visible_and_displayed(RiskPOCLocators.ADD_CPT_LINK),
            "Switch to old view link": self.is_visible_and_displayed(RiskPOCLocators.SWITCH_TO_OLD_VIEW_LINK),
            "Date of Service text field and label":
                (self.is_visible_and_displayed(RiskPOCLocators.DOS_FIELD)
                and self.is_visible_and_displayed(RiskPOCLocators.DOS_LABEL)),
            "Delete button": self.is_visible_and_displayed(RiskPOCLocators.DELETE),
            "Rendering Provider text field and label": (
                    self.is_visible_and_displayed(RiskPOCLocators.RENDERING_PROVIDER_FIELD)
                    and self.is_visible_and_displayed(RiskPOCLocators.RENDERING_PROVIDER_LABEL)
            ),
            "Save Draft button": self.is_visible_and_displayed(RiskPOCLocators.SAVE_DRAFT_BUTTON),
            "Submit button": self.is_visible_and_displayed(RiskPOCLocators.SUBMIT_BUTTON),
            "Disclaimer Link": self.is_visible_and_displayed(RiskPOCLocators.DISCLAIMER_LINK),
            "Attachment Section": (self.is_visible_and_displayed(RiskPOCLocators.ATTACHMENT_HEADER)
        and self.is_visible_and_displayed(RiskPOCLocators.ATTACHMENT_SECTION_PATIENT_DOCUMENTS)
        and self.is_visible_and_displayed(RiskPOCLocators.ATTACHMENT_SECTION_CSG) )

        }
        #webfunctions.debug_locator(RiskPOCLocators.ATTACHMENT_SECTION_FILE, "fileupload")
        return checks



    def is_risk_label_visible(self) -> bool:
        """Return True if the risk label element is displayed (handles waiting)."""
        el = self.wait_for_element(RiskPOCLocators.RISK_LABEL)
        return el.is_displayed() if el else False

    def get_risk_label_text(self) -> str:
        """Return the text of the risk label (empty string if not found)."""
        el = self.wait_for_element(RiskPOCLocators.RISK_LABEL)
        return el.text.strip() if el else ""

    def get_risk_count(self) -> int:
        """
        Parse and return the count displayed on the page as an int.
        Return -1 or 0 if not present depending on your convention.
        """
        el = self.wait_for_element(RiskPOCLocators.RISK_COUNT)
        if not el:
            return -1
        text = el.text.strip()
        return int(text)

    def click_visible_show_dx_buttons(self):
        """
        Wait until any Show DX button is visible,
        then click all displayed ones.
        """


        print("Waiting for show dx button to be visible")
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_any_elements_located(RiskPOCLocators.SHOW_DX_BUTTON)
        )
        print("Show dx is visible")
        buttons = self.driver.find_elements(*RiskPOCLocators.SHOW_DX_BUTTON)
        clicked = 0
        for btn in buttons:
            if btn.is_displayed():
                print("Going to click on button")
                webfunctions.action_click(self.driver, btn)
                clicked += 1
            # 🔑 wait for result of the click
            # 🔑 Wait until count increases

        return clicked



    def get_visible_poc_dx_texts(self) -> list[str]:
        """
        Returns visible POC DX texts.
        """
        # try:
        #     WebDriverWait(self.driver, 10).until(
        #         EC.visibility_of_any_elements_located(RiskPOCLocators.POC_DX)
        #     )
        # except:
        #     return []

        poc_dx_elements = self.driver.find_elements(*RiskPOCLocators.POC_DX)
        print(f"Number of dx elements in POC {len(poc_dx_elements)} ")
        return [el.text for el in poc_dx_elements if el.is_displayed()]


    def get_hcc_list(self):
        """ contains list of HCCs displayed in POC """
        list_hcc_elements=self.driver.find_elements(*RiskPOCLocators.DISPLAYED_HCCS)
        list_hccs=[]
        for hcc_element in list_hcc_elements :
            hcc_info_list=[]
            hcc_info_str=hcc_element.get_attribute("data-hcc_info")
            hcc_info=json.loads(hcc_info_str)
            hcc_id=hcc_info["hcc_id"]
            hcc_desc = hcc_info["hcc_desc"]
            # hcc_desc=hcc_info["hcc_id"]
            hcc_info_list.append(hcc_id)
            # description assumes its V28 model
            hcc_info_list.append(hcc_desc)
            list_hccs.append(hcc_info_list)
        # print(list_hccs)
        return list_hccs

    def get_dx_dos_rows(self):
        """
    Returns:
    [
      (hcc_name, hcc_number,hcc_desc,dx_description, dx_code, last_dos),
      (hcc_name, hcc_number,hcc_desc,dx_description, dx_code, last_dos),
      ...
    ]
    """
        hcc_list=self.get_hcc_list()
        # print(f"Number of hccs : {hcc_list}")
        dx_dos_rows=[]
        for i in range(1,len(hcc_list)+1):
            dx_code_description_s=f"//div[contains(@class,'clear hcc_row plm') and not(contains(@class, 'hide'))][{i}]//child::div[@class='col dx_description pbs mwidth']"
            dx_code_s = f"//div[contains(@class,'clear hcc_row plm') and not(contains(@class, 'hide'))][{i}]//child::div[@class='dx_code_div gray_background']"
            last_dos_s =f"//div[contains(@class,'clear hcc_row plm') and not(contains(@class, 'hide'))][{i}]//child::div[@data-tooltip='Last DOS']"
            number_of_codes=len(self.driver.find_elements(By.XPATH,dx_code_description_s))
            if hcc_list[i-1][0]!=0 :
                hcc_id = hcc_list[i - 1][0].split("(")[0]
                hcc_desc = hcc_list[i - 1][1]
            else:
                hcc_id="0"
                hcc_desc="No HCC"
            for j in range(1,number_of_codes+1):
                dx_desc_xpath = f"({dx_code_description_s})[{j}]"
                dx_code_xpath = f"({dx_code_s})[{j}]"
                last_dost_xpath= f"({last_dos_s})[{j}]"
                dx_description = self.driver.find_element(By.XPATH, dx_desc_xpath).text.strip()
                dx_code = self.driver.find_element(By.XPATH, dx_code_xpath).text.strip()
                elements = self.driver.find_elements(By.XPATH, last_dost_xpath)
                if elements:
                    last_dos = elements[0].text.strip()
                else:
                    last_dos = "Not Present"
                dx_dos_rows.append(
                    (hcc_id,hcc_desc,dx_description, dx_code, last_dos)
                )
        #print(dx_dos_rows)
        return dx_dos_rows

    def get_notification_if_present(self, timeout=10):
        """
        Waits for notification toast.
        Returns notification text if present,
        else returns None.
        Does NOT raise.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    RiskPOCLocators.DRUPAL_ALERT
                )
            )

            return (
                self.driver
                .find_element(*RiskPOCLocators.DRUPAL_ALERT)
                .text
                .strip()
            )

        except TimeoutException:
            return None


    def get_hcc_hierarchies(self):
        """Get all the hierarchies in a POC form """
        list_hierarchies=self.driver.find_elements(*RiskPOCLocators.HCC_HIERARCHIES)
        hierarchy_names=[]
        for hierarchy in list_hierarchies :
            if hierarchy.is_displayed():
                hierarchy_names.append(hierarchy.text)
        return hierarchy_names

    def get_attachment_input(self):
        return self.driver.find_element(*RiskPOCLocators.ATTACHMENT_SECTION_FILE)

    def get_attached_file_name(self):
        uploaded_files=self.driver.find_elements(*RiskPOCLocators.ATTACHED_FILE_NAMES)
        file_names=[]
        for file in uploaded_files :
            file_names.append(file.text.strip())
        return file_names

    def is_add_document_available(self):
        """
        Checks whether 'Add Document' button is visible in UI.
        Returns True if visible, else False.
        """
        try:
            el = self.driver.find_element(*RiskPOCLocators.ADD_DOCUMENT_BUTTON)

            # Fast path: Selenium visibility
            if el.is_displayed():
                return True

            # Fallback: JS visibility (covers CSS-hidden cases)
            return self.driver.execute_script(
                """
                const e = arguments[0];
                const s = window.getComputedStyle(e);
                const r = e.getBoundingClientRect();
                return (
                    s.display !== 'none' &&
                    s.visibility !== 'hidden' &&
                    s.opacity !== '0' &&
                    r.width > 0 &&
                    r.height > 0
                );
                """,
                el
            )

        except NoSuchElementException:
            return False

    def get_suspect_reason_modal_data(self):
        """
        Opens the suspect reason modal (if available), captures its content,
        closes the modal, and returns the data as a string.
        """
        suspect_reasons = self.driver.find_elements(*RiskPOCLocators.SUSPECT_REASON)
        # webfunctions.debug_locator(self.driver, RiskPOCLocators.SUSPECT_REASON, "suspect_reason")
        if not suspect_reasons:
            return ""

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(RiskPOCLocators.SUSPECT_REASON)
            )

            try:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    suspect_reasons[0]
                )
                suspect_reasons[0].click()
                time.sleep(2)
            except ElementClickInterceptedException:
                # Fallback for icon / overlay issues
                webfunctions.action_click(self.driver,suspect_reasons[0])
                time.sleep(2)


            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    RiskPOCLocators.SUSPECT_REASON_MODAL
                )
            )

            header = self.driver.find_element(
                *RiskPOCLocators.SUSPECT_REASON_HEADER_CONTENT
            ).text

            content = self.driver.find_element(
                *RiskPOCLocators.SUSPECT_REASON_MODAL_CONTENT
            ).text

            return f"Header: {header}\nContent: {content}"

        except TimeoutException:
            return ""

        finally:
            close_buttons = self.driver.find_elements(
                *RiskPOCLocators.SUSPECT_REASON_MODAL_CLOSE
            )
            if close_buttons:
                self.driver.execute_script(
                    "arguments[0].click();", close_buttons[0]
                )

    def get_all_hcc_list(self):
        all_hcc=self.driver.find_element(*RiskPOCLocators.ALL_HCCS_TOGGLE)
        all_hcc.click()
        time.sleep(2)
        number_of_hccs=len(self.get_hcc_list())
        all_hcc.click()
        return number_of_hccs

    def get_all_dx(self):
        dx_code_elements=self.driver.find_elements(*RiskPOCLocators.ALL_DX)
        dx_codes=[]
        for dx_code_element in dx_code_elements:
            raw_code=dx_code_element.text
            formatted_code=raw_code.replace(".","")
            dx_codes.append(formatted_code)
        return dx_codes

    def _close_dx_modal(self):
        close_buttons = self.driver.find_elements(*RiskPOCLocators.DX_CLOSE_MODAL)
        if close_buttons:
            webfunctions.action_click(self.driver, close_buttons[0])

        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(RiskPOCLocators.ADD_DX_MODAL_INPUT)
        )

    def add_cpt(self,cpt):
        """
               Opens Add CPT modal, searches CPT code, adds it if found.
               Closes modal safely if CPT is not found.
               Returns True if CPT is added, else False.
               """

        # Open modal
        self.driver.find_element(*RiskPOCLocators.ADD_CPT_BUTTON).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(RiskPOCLocators.ADD_CPT_MODAL_INPUT)
        )

        add_cpt_input = self.driver.find_element(*RiskPOCLocators.ADD_CPT_MODAL_INPUT)
        add_cpt_input.clear()
        time.sleep(2)
        webfunctions.action_click(self.driver, add_cpt_input)
        time.sleep(2)
        webfunctions.sendkeys(self.driver, add_cpt_input, cpt)
        time.sleep(2)
        webfunctions.action_click(self.driver, add_cpt_input)
        time.sleep(2)
        # Try waiting for search results (soft wait)
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(RiskPOCLocators.CPT_SEARCH_RESULTS)
            )
        except TimeoutException:
            # ❗ No search results appeared → close modal
            self._close_dx_modal()
            return False

        search_results = self.driver.find_elements(*RiskPOCLocators.CPT_SEARCH_RESULTS)

        result_clicked = False

        for search_result in search_results:
            result_id = search_result.get_attribute("id")
            info_list = [p for p in result_id.split("|") if p]

            result_code = info_list[0]

            if result_code == cpt:
                webfunctions.action_click(self.driver, search_result)
                result_clicked = True
                break

        # ❗ If no matching DX found → close modal
        if not result_clicked:
            self._close_dx_modal()
            return False

        return cpt in self.get_all_dx()

    def get_cpts(self):
        """Gets all the CPT info displayed in POC form , in form of tag,description,code"""
        list_cpt_row = self.driver.find_element(*RiskPOCLocators.DISPLAYED_CPT)
        cpt_tag=self.driver.find_element(*RiskPOCLocators.CPT_TAG).text.strip()
        list_cpt_rows=self.driver.find_elements(*RiskPOCLocators.CPT_ROWS)
        list_cpt_code = []
        for list_cpt_row in list_cpt_rows:
            cpt_info_list=[]
            cpt_description=list_cpt_row.find_element(*RiskPOCLocators.CPT_DESCRIPTION).text
            cpt_code=list_cpt_row.find_element(*RiskPOCLocators.CPT_CODE).text
            cpt_info_list.append(cpt_tag)
            cpt_info_list.append(cpt_description)
            cpt_info_list.append(cpt_code)
            list_cpt_code.append(cpt_info_list)
        # print(list_hccs)
        return list_cpt_code



    def add_dx_global(self, dx_code, hcc_linked):
        """
        Opens Add DX modal, searches DX code, adds it if found.
        Closes modal safely if DX is not found.
        Returns True if DX is added, else False.
        """

        # Open modal
        self.driver.find_element(*RiskPOCLocators.ADD_DX_BUTTON).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(RiskPOCLocators.ADD_DX_MODAL_INPUT)
        )

        add_dx_input = self.driver.find_element(*RiskPOCLocators.ADD_DX_MODAL_INPUT)
        add_dx_input.clear()
        time.sleep(2)
        webfunctions.action_click(self.driver, add_dx_input)
        time.sleep(2)
        webfunctions.sendkeys(self.driver, add_dx_input, dx_code)
        time.sleep(2)
        webfunctions.action_click(self.driver, add_dx_input)


        # Try waiting for search results (soft wait)
        try:
            wait = WebDriverWait(self.driver, 15)
            result = wait.until(
                EC.any_of(
                    EC.visibility_of_element_located(RiskPOCLocators.DX_SEARCH_RESULTS),
                    EC.visibility_of_element_located(RiskPOCLocators.DX_SEARCH_NOT_FOUND),
                )
            )

        except TimeoutException:
            # ❗ No search results appeared → close modal
            self._close_dx_modal()
            return False
        result_clicked = False
        if result.find_elements(*RiskPOCLocators.DX_SEARCH_RESULTS):
            print("Search result appeared")
            search_results = self.driver.find_elements(*RiskPOCLocators.DX_SEARCH_RESULTS)
            for search_result in search_results:
                result_id = search_result.get_attribute("id")
                info_list = [p for p in result_id.split("|") if p]
                result_code = info_list[3] if hcc_linked else info_list[0]
                if result_code.replace(".", "") == dx_code:
                    webfunctions.action_click(self.driver, search_result)
                    result_clicked = True
                    print("Result Clicked")
                    break

        else:
            time.sleep(2)
            self._close_dx_modal()
            print("No suggestion found ")
            return False


        # ❗ If no matching DX found → close modal
        if not result_clicked:
            time.sleep(2)
            self._close_dx_modal()
            return False
        time.sleep(1)
        return dx_code in self.get_all_dx()

    # def add_dx_first_row
    def is_disconfirm_button_disabled(self, dx_code):
        xpath = f"//div[text()='{dx_code}']//ancestor::div[contains(@class,'hcc_row')]//child::div[contains(@class,'action_btn') and contains(@class,'disconfirm_btn')]"
        btn = self.driver.find_element(By.XPATH, xpath)
        classes = btn.get_attribute("class")
        return "hcc_custom_disabled" in classes

    def is_not_addressed_button_disabled(self, dx_code):
        xpath = f"//div[text()='{dx_code}']//ancestor::div[contains(@class,'hcc_row')]//child::div[contains(@class,'action_btn') and contains(@class,'deferred_btn')]"
        btn = self.driver.find_element(By.XPATH, xpath)
        return "hcc_custom_disabled" in btn.get_attribute("class")

    def recapture_disconfirm(self):
        """
        Finds the first Recapture DX with enabled Disconfirm action,
        performs Disconfirm, and returns observed UI state.
        Returns None if no eligible DX is found.
        """

        dx_rows = self.get_dx_dos_rows()

        for hcc_id, hcc_desc, dx_description, dx_code, last_dos in dx_rows:

            # --- Read HCC tag ---
            hcc_tag_xpath = (
                f"//div[text()='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
                "//div[contains(@class,'careops-new tooltipped')]"
            )

            hcc_tag_elements = self.driver.find_elements(By.XPATH, hcc_tag_xpath)
            if not hcc_tag_elements:
                continue

            if hcc_tag_elements[0].text.strip() != "Recapture":
                continue



            # --- Locate Disconfirm button ---
            disconfirm_xpath = (
                f"//div[@id='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
                "//div[contains(@class,'action_btn disconfirm_btn')]"
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                hcc_tag_elements[0]
            )

            disconfirm_elements = self.driver.find_elements(By.XPATH, disconfirm_xpath)
            if not disconfirm_elements:
                continue

            disconfirm_button = disconfirm_elements[0]
            disconfirm_classes = disconfirm_button.get_attribute("class")

            if "hcc_custom_disabled" in disconfirm_classes:
                continue

            # --- Perform Disconfirm ---
            webfunctions.action_click(self.driver, disconfirm_button)

            # --- Observe DOT status ---
            dot_status = "unknown"
            hcc_dot_xpath = (
                f"//div[text()='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
                "//div[contains(@class,'dot_status')]"
            )

            dot_elements = self.driver.find_elements(By.XPATH, hcc_dot_xpath)
            if dot_elements:
                dot_classes = dot_elements[0].get_attribute("class")
                dot_status = "no dot" if "no_dot" in dot_classes else "present"

            # --- Observe Disconfirm tag ---
            disconfirm_tag_text = None
            disconfirm_tag_xpath = (
                f"//div[text()='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
                "//div[contains(@class,'disconfirm_tag') and not(contains(@class,'hide'))]"
                "//span"
            )

            disconfirm_tag_elements = self.driver.find_elements(
                By.XPATH, disconfirm_tag_xpath
            )
            if disconfirm_tag_elements:
                disconfirm_tag_text = disconfirm_tag_elements[0].text.strip()

            # --- Observe Undo Disconfirm ---

            # 1️⃣ Scroll ENTIRE ROW into view
            hcc_row_xpath = (
                f"//div[text()='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
            )

            hcc_row = self.driver.find_element(By.XPATH, hcc_row_xpath)


            # 2️⃣ Locate Undo button (parent)
            undo_btn_xpath = (
                    hcc_row_xpath +
                    "//div[contains(@class,'action_btn') and contains(@class,'undo_disconfirm')]"
            )
            # 3️⃣ Move mouse to ROW first (important for grid UIs)


            undo_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, undo_btn_xpath))
            )

            # 1️⃣ Scroll undo button into viewport
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", undo_btn
            )

            # 2️⃣ Hover row → then button → pause
            ActionChains(self.driver) \
                .move_to_element(hcc_row) \
                .pause(0.3) \
                .move_to_element(undo_btn) \
                .pause(4) \
                .perform()

            # 4️⃣ Wait for text to APPEAR (presence → visibility)
            undo_text_xpath = (
                    undo_btn_xpath +
                    "//span[contains(@class,'btn_title')]"
            )

            undo_text_el =webfunctions.wait_or_scroll_to_element(self.driver, undo_text_xpath)

            undo_disconfirm_text = undo_text_el.text.strip()

            # --- Return observed facts ---
            return {
                "dx_code": dx_code,
                "hcc_id": hcc_id,
                "dot_status": dot_status,
                "disconfirm_tag_text": disconfirm_tag_text,
                "undo_disconfirm_text": undo_disconfirm_text,
            }

        return None

    def mark_as_not_addressed(self):
        """
        Finds the first Recapture DX with enabled Mark As Not Addressed action,
        performs Not Addressed, and returns observed UI state.
        Returns None if no eligible DX is found.
        """

        dx_rows = self.get_dx_dos_rows()

        for hcc_id, hcc_desc, dx_description, dx_code, last_dos in dx_rows:
            print(f"{dx_code} dx code" )
            # --- Read HCC tag ---
            hcc_tag_xpath = (
                f"//div[text()='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
                "//div[contains(@class,'careops-new tooltipped')]"
            )

            hcc_tag_elements = self.driver.find_elements(By.XPATH, hcc_tag_xpath)
            if not hcc_tag_elements:
                print(f"No selected")
                continue

            if hcc_tag_elements[0].text.strip() != "Recapture":
                print(f"Not selected")
                continue

            # --- Observe Disconfirm tag ---
            disconfirm_tag_text = None
            disconfirm_tag_xpath = (
                f"//div[text()='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
                "//div[contains(@class,'disconfirm_tag') and not(contains(@class,'hide'))]"
                "//span"
            )

            disconfirm_tag_elements = self.driver.find_elements(
                By.XPATH, disconfirm_tag_xpath
            )
            if disconfirm_tag_elements:
                continue

        # --- Check if not disconfirmed -------------




            # --- Locate Not Addressed button ---
            not_addressed_xpath = (
                f"//div[@id='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
                "//div[contains(@class,'action_btn deferred_btn ')]"
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                hcc_tag_elements[0]
            )

            not_addressed_elements = self.driver.find_elements(By.XPATH, not_addressed_xpath)
            if not not_addressed_elements:
                continue

            not_addressed_button = not_addressed_elements[0]
            not_addressed_classes = not_addressed_button.get_attribute("class")

            if "hcc_custom_disabled" in not_addressed_classes:
                continue

            # --- Perform Disconfirm ---
            webfunctions.action_click(self.driver, not_addressed_button)

            # --- Observe DOT status ---
            dot_status = "unknown"
            hcc_dot_xpath = (
                f"//div[text()='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
                "//div[contains(@class,'dot_status')]"
            )

            dot_elements = self.driver.find_elements(By.XPATH, hcc_dot_xpath)
            if dot_elements:
                dot_classes = dot_elements[0].get_attribute("class")
                dot_status = "no dot" if "no_dot" in dot_classes else "present"

            # --- Observe  tag ---
            not_addressed_text = None
            not_addressed_tag_xpath = (
                f"//div[text()='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
                "//div[contains(@class,'deferred_tag') and not(contains(@class,'hide'))]"
                "//span"
            )

            not_addressed_tag_elements = self.driver.find_elements(
                By.XPATH, not_addressed_tag_xpath
            )
            if not_addressed_tag_elements:
                not_addressed_tag_text = not_addressed_tag_elements[0].text.strip()

            # --- Observe Undo  ---

            # 1️⃣ Scroll ENTIRE ROW into view
            hcc_row_xpath = (
                f"//div[text()='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
            )

            hcc_row = self.driver.find_element(By.XPATH, hcc_row_xpath)


            # 2️⃣ Locate Undo button (parent)
            undo_deferred_xpath = (
                    hcc_row_xpath +
                    "//div[contains(@class,'action_btn') and contains(@class,'undo_deferred')]"
            )
            # 3️⃣ Move mouse to ROW first (important for grid UIs)


            undo_deferred_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, undo_deferred_xpath))
            )

            # 1️⃣ Scroll undo button into viewport
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", undo_deferred_btn
            )

            # 2️⃣ Hover row → then button → pause
            ActionChains(self.driver) \
                .move_to_element(hcc_row) \
                .pause(0.3) \
                .move_to_element(undo_deferred_btn) \
                .pause(4) \
                .perform()

            # 4️⃣ Wait for text to APPEAR (presence → visibility)
            undo_text_xpath = (
                    undo_deferred_xpath +
                    "//span[contains(@class,'btn_title')]"
            )

            undo_text_el =webfunctions.wait_or_scroll_to_element(self.driver, undo_text_xpath)

            undo_deferred_text = undo_text_el.text.strip()

            # --- Return observed facts ---
            return {
                "dx_code": dx_code,
                "hcc_id": hcc_id,
                "dot_status": dot_status,
                "not_addressed_tag_text": not_addressed_tag_text,
                "undo_deferred_text": undo_deferred_text,
            }

        return None
    def is_print_hcc_visible(self, timeout=5):
        """
        Returns True if Print HCC button is clickable, else False.
        Does NOT raise.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(RiskPOCLocators.PRINT_BUTTON)
            )
            return True
        except TimeoutException:
            return False

    def get_kebab_menu_options(self):
        """
        Clicks kebab menu and returns list of visible option texts.
        Does NOT assert.
        """

        kebab_icon = self.driver.find_element(
            *RiskPOCLocators.KEBAB_MENU_ICON
        )
        webfunctions.action_click(self.driver, kebab_icon)

        # Wait until at least one menu option is visible
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_any_elements_located(
                RiskPOCLocators.KEBAB_MENU_OPTIONS
            )
        )

        options = self.driver.find_elements(
            *RiskPOCLocators.KEBAB_MENU_OPTIONS
        )
        time.sleep(3)
        webfunctions.action_click(self.driver, kebab_icon)

        return [
            option.text.strip()
            for option in options
            if option.text.strip()
        ]


    def recapture_confirm(self):
        """
        Confirms the first Recapture DX found.
        Returns context dict if action taken,
        else returns None.
        """

        dx_desc_last_dos = self.get_dx_dos_rows()

        for hcc_id, hcc_desc, dx_description, dx_code, last_dos in dx_desc_last_dos:

            hcc_tag_xpath = (
                f"//*[text()='{dx_code}']"
                "//ancestor::div[contains(@class,'hcc_row')]"
                "//div[contains(@class,'careops-new tooltipped')]"
            )
            print("Waiting for hcc tag to be found")
            webfunctions.wait_or_scroll_to_element(self.driver,hcc_tag_xpath)
            print("HCC Tag is visible ")
            hcc_tag = self.driver.find_element(By.XPATH, hcc_tag_xpath).text.strip()
            print(f"HCC Tag is {hcc_tag} ")
            if hcc_tag == "Recapture":
                confirm_xpath = (
                    f"//div[@id='{dx_code}']"
                    "//i[contains(@class,'custom_confirm')]"
                )

                confirm_icon = self.driver.find_element(By.XPATH, confirm_xpath)
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center', inline:'nearest'});",
                    confirm_icon
                )
                webfunctions.action_click(self.driver, confirm_icon)

                # Check red dot or hollow dot near HCC
                hcc_dot_xpath = (
                    f"//div[text()='{dx_code}']"
                    "//ancestor::div[contains(@class,'hcc_row')]"
                    "//div[contains(@class,'dot_status')]"
                )

                dot_status = None  # default

                dot_element = self.driver.find_element(By.XPATH, hcc_dot_xpath)
                dot_classes = dot_element.get_attribute("class")

                if "hollow_red" in dot_classes:
                    dot_status = "hollow"
                else:
                    dot_status = "solid"

                return {
                    "dx_code": dx_code,
                    "hcc_id": hcc_id,
                    "dx_description": dx_description,
                    "last_dos": last_dos,
                    "dot_status": dot_status
                }

        return None




        # try:
        #     # Wait for POC body to be present
        #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.POC_BODY))
        #
        #     # find the recapture tag
        #     tag_el = self.driver.find_element(*RiskPOCLocators.RECAPTURE_TAG)
        #
        #     # ensure the tooltip locator is defined
        #     if not RiskPOCLocators.CONFIRM_TOOLTIP:
        #         raise ValueError("CONFIRM_TOOLTIP locator is not defined in RiskPOCLocators")
        #
        #     # find and click the confirm tooltip inside the tag
        #     tooltip_el = tag_el.find_element(*RiskPOCLocators.CONFIRM_TOOLTIP)
        #     try:
        #         webfunctions.action_click(self.driver, tooltip_el)
        #     except Exception:
        #         tooltip_el.click()
        #
        #     print("Recapture Confirmed Successfully.")
        # except Exception as e:
        #     print("Recapture Confirm Failed:", e)

    # def RecaptureDisconfirm(self):
    #     try:
    #         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.POC_BODY))
    #
    #         tag_el = self.driver.find_element(*RiskPOCLocators.RECAPTURE_TAG)
    #
    #         if not RiskPOCLocators.DISCONFIRM_TOOLTIP:
    #             raise ValueError("DISCONFIRM_TOOLTIP locator is not defined in RiskPOCLocators")
    #
    #         tooltip_el = tag_el.find_element(*RiskPOCLocators.DISCONFIRM_TOOLTIP)
    #         try:
    #             webfunctions.action_click(self.driver, tooltip_el)
    #         except Exception:
    #             tooltip_el.click()
    #
    #         print("Recapture Disconfirmed Successfully.")
    #     except Exception as e:
    #         print("Recapture Disconfirm Failed:", e)

    def RecaptureNotAddressed(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.POC_BODY))

            tag_el = self.driver.find_element(*RiskPOCLocators.RECAPTURE_TAG)

            if not RiskPOCLocators.NOT_ADDRESSED_TOOLTIP:
                raise ValueError("NOT_ADDRESSED_TOOLTIP locator is not defined in RiskPOCLocators")

            tooltip_el = tag_el.find_element(*RiskPOCLocators.NOT_ADDRESSED_TOOLTIP)
            try:
                webfunctions.action_click(self.driver, tooltip_el)
            except Exception:
                tooltip_el.click()

            print("Recapture Marked as Not Addressed Successfully.")
        except Exception as e:
            print("Recapture Not Addressed Failed:", e)

    def SuspectConfirm(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.POC_BODY))

            tag_el = self.driver.find_element(*RiskPOCLocators.SUSPECT_TAG)

            if not RiskPOCLocators.CONFIRM_TOOLTIP:
                raise ValueError("CONFIRM_TOOLTIP locator is not defined in RiskPOCLocators")

            tooltip_el = tag_el.find_element(*RiskPOCLocators.CONFIRM_TOOLTIP)
            try:
                webfunctions.action_click(self.driver, tooltip_el)
            except Exception:
                tooltip_el.click()

            print("Suspect Confirmed Successfully.")
        except Exception as e:
            print("Suspect Confirm Failed:", e)

    def SuspectDisconfirm(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.POC_BODY))

            tag_el = self.driver.find_element(*RiskPOCLocators.SUSPECT_TAG)

            if not RiskPOCLocators.DISCONFIRM_TOOLTIP:
                raise ValueError("DISCONFIRM_TOOLTIP locator is not defined in RiskPOCLocators")

            tooltip_el = tag_el.find_element(*RiskPOCLocators.DISCONFIRM_TOOLTIP)
            try:
                webfunctions.action_click(self.driver, tooltip_el)
            except Exception:
                tooltip_el.click()

            print("Suspect Disconfirmed Successfully.")
        except Exception as e:
            print("Suspect Disconfirm Failed:", e)

    def SuspectNotAddressed(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.POC_BODY))

            tag_el = self.driver.find_element(*RiskPOCLocators.SUSPECT_TAG)

            if not RiskPOCLocators.NOT_ADDRESSED_TOOLTIP:
                raise ValueError("NOT_ADDRESSED_TOOLTIP locator is not defined in RiskPOCLocators")

            tooltip_el = tag_el.find_element(*RiskPOCLocators.NOT_ADDRESSED_TOOLTIP)
            try:
                webfunctions.action_click(self.driver, tooltip_el)
            except Exception:
                tooltip_el.click()

            print("Suspect Marked as Not Addressed Successfully.")
        except Exception as e:
            print("Suspect Not Addressed Failed:", e)

    def AddDiagnosis(self, data):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.POC_BODY))

            if not RiskPOCLocators.ADD_DX_BUTTON:
                raise ValueError("ADD_DX_BUTTON locator is not defined in RiskPOCLocators")

            # open add diagnosis modal
            add_btn = self.driver.find_element(*RiskPOCLocators.ADD_DX_BUTTON)
            try:
                webfunctions.action_click(self.driver, add_btn)
            except Exception:
                add_btn.click()
            print("Add Diagnosis Button Clicked Successfully.")

            # type diagnosis code and pick from the suggestion list
            self.driver.find_element(*RiskPOCLocators.ADD_DX_MODAL_INPUT).send_keys(data.dx_code)

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.ADD_DX_MODAL_LIST))
            suggestions = self.driver.find_element(*RiskPOCLocators.ADD_DX_MODAL_LIST).find_elements(By.TAG_NAME, "li")
            if len(suggestions) > 1:
                suggestions[1].click()
            else:
                suggestions[0].click()
            print("Diagnosis Added Successfully.")
        except Exception as e:
            print("Add Diagnosis Failed:", e)

    # def getNotes(self):

    def addNote(self, data):
        result = {
            "note_modal_appeared": False,
            "note_modal_header": False,
            "note_shortcut_label": False,
            "note_modal_suggestions": False
        }

        try:
            add_note_btn = self.driver.find_element(*RiskPOCLocators.ADD_NOTE_BUTTON)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", add_note_btn
            )
            try:
                webfunctions.action_click(self.driver, add_note_btn)
                print("Clicked on note icon")
            except Exception:
                print("Add Note button not clicked")
                add_note_btn.click()



            # Wait for note textarea (modal appeared)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(RiskPOCLocators.NOTE_TEXTAREA)
            )
            result["note_modal_appeared"] = True
            print("Add Note modal appeared.")

            # Header check
            if self.driver.find_elements(*RiskPOCLocators.NOTE_HEADER):
                result["note_modal_header"] = True

            # Shortcut label check
            if self.driver.find_elements(*RiskPOCLocators.NOTE_SHORTCUT_LABEL):
                result["note_shortcut_label"] = True

            note_textarea = self.driver.find_element(*RiskPOCLocators.NOTE_TEXTAREA)
            note_textarea.send_keys("@")
            webfunctions.move_cursor_space_and_backspace(note_textarea)
            time.sleep(1)
            note_textarea.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(RiskPOCLocators.NOTE_SUGGESTIONS_LIST)
            )

            suggestions = self.driver.find_element(
                *RiskPOCLocators.NOTE_SUGGESTIONS_LIST
            ).find_elements(By.TAG_NAME, "li")

            if suggestions:
                suggestions[1].click() if len(suggestions) > 1 else suggestions[0].click()
                result["note_modal_suggestions"] = True
                print("Note suggestions selected.")

            note_textarea.clear()
            note_textarea.send_keys(data)

            self.driver.find_element(*RiskPOCLocators.NOTE_SAVE_BUTTON).click()
            print("Note added successfully.")

            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element(RiskPOCLocators.NOTE_HEADER))
            return result

        except Exception as e:
            print("Add Note failed:", e)
            return result

    def check_if_note_icon_displayed(self):
        return len(self.driver.find_elements(*RiskPOCLocators.VISIBLE_NOTES))



    def SetDOS(self, data):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.POC_BODY))
            dos_field = self.driver.find_element(*RiskPOCLocators.DOS_FIELD)
            dos_field.clear()
            dos_field.send_keys(data.dos_field)
            print("Date of Service Set Successfully.")
        except Exception as e:
            print("Set Date of Service Failed:", e)

    def SetProvider(self, data):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.POC_BODY))

            provider_field = self.driver.find_element(*RiskPOCLocators.PROVIDER_FIELD)
            provider_field.clear()
            provider_field.send_keys(data.provider_name)

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.PROVIDER_LIST))
            provider_items = self.driver.find_element(*RiskPOCLocators.PROVIDER_LIST).find_elements(By.TAG_NAME, "li")
            if len(provider_items) > 1:
                provider_items[1].click()
            else:
                provider_items[0].click()

            print("Provider Set Successfully.")
        except Exception as e:
            print("Set Provider Failed:", e)

    def SaveDraftPOC(self):
        """
        Clicks Save Draft and returns autosave details.

        Returns:
        (status, autosave_icon, autosave_text, autosave_time)

        status: bool
        autosave_icon: str | None   -> expected "check"
        autosave_text: str | None
        autosave_time: str | None
        """
        try:
            # Click Save Draft
            webfunctions.action_click(
                self.driver,
                self.driver.find_element(*RiskPOCLocators.SAVE_DRAFT)
            )

            # Wait for Drupal alert
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(RiskPOCLocators.DRUPAL_ALERT)
            )

            notif = (
                self.driver
                .find_element(*RiskPOCLocators.DRUPAL_ALERT)
                .text
                .strip()
            )

            if "changes have been successfully saved" not in notif:
                return False, None, None, None

            # Read autosave UI values
            autosave_icon = (
                self.driver
                .find_element(*RiskPOCLocators.AUTOSAVE_ICON)
                .text
                .strip()
            )

            autosave_text = (
                self.driver
                .find_element(*RiskPOCLocators.AUTOSAVE_TEXT)
                .text
                .strip()
            )

            autosave_time = (
                self.driver
                .find_element(*RiskPOCLocators.AUTOSAVE_TIME)
                .text
                .strip()
            )

            return True, autosave_icon, autosave_text, autosave_time

        except Exception:
            return False, None, None, None

    def close_date_picker(self):
        try :
            webfunctions.action_click(self.driver, self.driver.find_element(*RiskPOCLocators.FOOTER))
            return True
        except Exception as e:
            return False

    def get_enabled_years_in_date_picker(self):
        webfunctions.action_click(
            self.driver,
            self.driver.find_element(*RiskPOCLocators.VISIBLE_YEAR_DATEPICKER)
        )
        # Wait until at least one enabled year is present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                RiskPOCLocators.ENABLED_YEAR_DATEPICKER
            )
        )
        elements = self.driver.find_elements(
            *RiskPOCLocators.ENABLED_YEAR_DATEPICKER
        )
        time.sleep(2)
        return [el.text.strip() for el in elements if el.text.strip()]



    def is_dos_date_picker_open(self):
        return len(self.driver.find_elements(*RiskPOCLocators.DATE_PICKER)) > 0

    def get_dos_field(self):
        return self.driver.find_element(*RiskPOCLocators.DOS_FIELD)

    def _click_dos_field(self, wait):
        try:
            print("[set_dos] Waiting for DOS field to be clickable")
            dos_field = wait.until(
                EC.element_to_be_clickable(RiskPOCLocators.DOS_FIELD)
            )
            webfunctions.action_click(self.driver, dos_field)
            print("[set_dos] DOS field clicked")
            return True
        except Exception as e:
            print(f"[set_dos][ERROR] Failed to click DOS field: {e}")
            return False

    def _wait_for_dos_date_picker(self, wait):
        try:
            print("[set_dos] Waiting for date picker to appear")
            wait.until(
                EC.visibility_of_element_located(RiskPOCLocators.DATE_PICKER)
            )
            print("[set_dos] Date picker is visible")
            return True
        except Exception as e:
            print(f"[set_dos][ERROR] Date picker did not appear: {e}")
            return False

    def _select_current_dos_date(self, wait):
        try:
            print("[set_dos] Waiting for current date to be clickable")
            current_date = wait.until(
                EC.element_to_be_clickable(RiskPOCLocators.CURRENT_DATE)
            )
            webfunctions.action_click(self.driver, current_date)
            print("[set_dos] Current date selected")
            return True
        except Exception as e:
            print(f"[set_dos][ERROR] Failed to select current date: {e}")
            return False

    def set_dos(self):
        print("[set_dos] Starting DOS selection flow")

        wait = WebDriverWait(self.driver, 10)

        if not self._click_dos_field(wait):
            return

        if not self._wait_for_dos_date_picker(wait):
            return

        if not self._select_current_dos_date(wait):
            return

        print("[set_dos] DOS selection completed successfully")

    def set_rendering_provider(self, provider_name):
        """
        Enters a searchable rendering provider name,
        selects the first result from the dropdown,
        and returns the number of results found.
        """

        provider_input = self.driver.find_element(
            *RiskPOCLocators.RENDERING_PROVIDER
        )
        provider_input.clear()
        provider_input.click()
        provider_input.send_keys(provider_name)

        wait = WebDriverWait(self.driver, 10)

        try:
            wait.until(
                EC.presence_of_element_located(
                    RiskPOCLocators.RENDERING_PROVIDER_SEARCH_RESULTS
                )
            )
        except TimeoutException:
            raise Exception(
                f"No rendering provider search results for: {provider_name}"
            )

        # 🔑 Fetch all results safely
        results = self.driver.find_elements(
            *RiskPOCLocators.RENDERING_PROVIDER_SEARCH_RESULTS
        )

        if not results:
            raise Exception(
                f"Rendering provider dropdown empty for: {provider_name}"
            )

        # Use first result only if results exist
        search_result = results[0]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            search_result
        )# Wait until a new window opens
        main_window = self.driver.current_window_handle
        existing_handles = set(self.driver.window_handles)
        webfunctions.action_click(self.driver, search_result)

        try:
            WebDriverWait(self.driver, 3).until(
                lambda d: len(d.window_handles) > len(existing_handles)
            )

            new_handles = set(self.driver.window_handles) - existing_handles

            for handle in new_handles:
                self.driver.switch_to.window(handle)
                self.driver.close()

            self.driver.switch_to.window(main_window)

        except TimeoutException:
            # No new tab opened → do nothing
            pass
        return len(results)

    def _collect_submission_context(self, wait, confirm_modal_appeared):
        """
        Collects submission-related data after submit flow.
        Does NOT click submit.
        """
        confirmed_hcc_list=[]
        confirmed_dx_list = []
        disconfirmed_hccs = []
        cpt_codes=[]
        not_addressed_hcc_list=[]

        # ---------- Collect Confirmed DXs ----------
        #print("Collected Confirmed DXs")
        confirmed_dxs = self.driver.find_elements(*RiskPOCLocators.CONFIRMED_DX_CHECKBOX)

        for dx in confirmed_dxs:
            dx_code = dx.get_attribute("dx_code") or dx.get_attribute("cpt_code")
            if dx_code:
                if dx.get_attribute("cpt_code") :
                    cpt_codes.append(dx_code)
                else:
                    confirmed_dx_list.append(dx_code)
                print(dx_code)

                hcc_row_xpath=f"//div[@dx_code='{dx_code}']//ancestor::div[contains(@class,'hcc_row ')]"
                print(hcc_row_xpath)
                try:
                    hcc_row = self.driver.find_element(By.XPATH,hcc_row_xpath)
                    print("hcc_row: found", hcc_row)
                    if hcc_row.get_attribute("data-hcc_info"):
                        hcc_info_raw = hcc_row.get_attribute("data-hcc_info")
                        hcc_info = json.loads(hcc_info_raw)
                        if hcc_info.get("hcc_id") != 0:
                            confirmed_hcc_list.append(hcc_info.get("hcc_id"))
                            print(f"hcc id parent {hcc_info.get('hcc_id')} ")
                except NoSuchElementException:
                    continue

        #print("Collected Confirmed DXs",confirmed_dxs)


        # ---------- Collect Not Addressed HCCs ----------
        visible_not_addressed_hccs = self.driver.find_elements(
            *RiskPOCLocators.VISIBLE_HCC_NOT_ADDRESSED
        )

        for hccs in visible_not_addressed_hccs:
            try:
                hcc_row = hccs.find_element(*RiskPOCLocators.PARENT_HCC_ROW)
                hcc_info_raw = hcc_row.get_attribute("data-hcc_info")
                hcc_info = json.loads(hcc_info_raw)
                if hcc_info.get("hcc_id"):
                    hcc_info = json.loads(hcc_info_raw)
                    print(f"Appending to not addressed {hcc_info.get('hcc_id')}")
                    not_addressed_hcc_list.append(hcc_info.get("hcc_id"))
            except (NoSuchElementException, json.JSONDecodeError):
                continue



        # ---------- Collect Disconfirmed HCCs ----------
        visible_disconfirmed_hccs = self.driver.find_elements(
            *RiskPOCLocators.VISIBLE_HCC_DISCONFIRM
        )
        print(len(visible_disconfirmed_hccs))
        for hcc in visible_disconfirmed_hccs:
            try:
                hcc_row = hcc.find_element(*RiskPOCLocators.PARENT_HCC_ROW)
                hcc_info_raw = hcc_row.get_attribute("data-hcc_info")
                print("Disconfirm blockj", hcc_info_raw)
                hcc_info = json.loads(hcc_info_raw)
                if hcc_info.get("hcc_id"):
                    hcc_info = json.loads(hcc_info_raw)
                    print(f"Appending to disconfirm {hcc_info.get('hcc_id')}")
                    disconfirmed_hccs.append(hcc_info.get("hcc_id"))
            except (NoSuchElementException, json.JSONDecodeError):
                continue

        # ---------- DOS & Rendering Provider ----------
        self.set_dos()

        dos_input = wait.until(
            EC.presence_of_element_located((By.ID, "enc_service_date"))
        )
        dos = dos_input.get_attribute("value")

        provider_input = wait.until(
            EC.presence_of_element_located(RiskPOCLocators.RENDERING_PROVIDER)
        )
        provider = provider_input.get_attribute("value")

        attachment_file_name=self.get_attached_file_name()

        return {
            "confirm_modal_appeared": confirm_modal_appeared,
            "confirmed_hccs":confirmed_hcc_list,
            "confirmed_dxs": confirmed_dx_list,
            "disconfirmed_hccs": disconfirmed_hccs,
            "date_of_service": dos,
            "rendering_provider": provider,
            "document_name":attachment_file_name,
            "cpt_codes":cpt_codes,
            "not_addressed_hcc_list":not_addressed_hcc_list
        }

    def SubmitPOC(self, invalid_submission=False):
        """
        Submits POC and returns submission context.
        Page layer does NOT assert.
        """

        full_text = None
        task_text = None
        task_href = None
        confirm_modal_appeared = False

        # ALWAYS define context
        context = {
            "confirm_modal_appeared": False,
            "confirmed_dxs": [],
            "disconfirmed_hccs": [],
            "date_of_service": "",
            "rendering_provider": "",
        }

        try:
            wait = WebDriverWait(self.driver, 15)

            # ---------- INVALID submission: click submit first ----------
            if invalid_submission:
                submit_btn = wait.until(
                    EC.element_to_be_clickable(RiskPOCLocators.SUBMIT_BUTTON)
                )
                webfunctions.action_click(self.driver, submit_btn)

                try:
                    confirm_modal = wait.until(
                        EC.visibility_of_element_located(RiskPOCLocators.CONFIRM_MODAL)
                    )
                    print("confirm_modal: asppeared ")
                    confirm_modal_appeared = True
                    confirm_submit = wait.until(
                        EC.element_to_be_clickable(RiskPOCLocators.CONFIRM_MODAL_SUBMIT)
                    )
                    webfunctions.action_click(self.driver, confirm_submit)
                    print("confirm_modal: clicked ")


                except TimeoutException:
                    print("Confirm modal not appeared")
                    pass

            # ---------- VALID submission: collect → submit ----------
            if not invalid_submission:
                context = self._collect_submission_context(wait, confirm_modal_appeared)

                submit_btn = wait.until(
                    EC.element_to_be_clickable(RiskPOCLocators.SUBMIT_BUTTON)
                )
                webfunctions.action_click(self.driver, submit_btn)

            # ---------- Notification (COMMON for both flows) ----------
            time.sleep(1)
            alert = wait.until(
                EC.presence_of_element_located(RiskPOCLocators.DRUPAL_ALERT)
            )

            full_text = alert.text.strip()

            links = alert.find_elements(By.TAG_NAME, "a")
            if links:
                task_text = links[0].text.strip()
                task_href = links[0].get_attribute("href")

            return {
                "notification": full_text,
                "notification_text": full_text,
                "task_text": task_text,
                "task_link": task_href,
                **context,
            }

        except Exception as e:
            return {
                "notification": full_text,
                "notification_text": full_text,
                "task_text": task_text,
                "task_link": task_href,
                **context,
                "error": str(e),
            }



    def DeletePOC(self, data):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.POC_BODY))
            self.driver.find_element(*RiskPOCLocators.DELETE).click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.DELETE_REASON_INPUT))
            self.driver.find_element(*RiskPOCLocators.DELETE_REASON_INPUT).send_keys(data.delete_reason)
            self.driver.find_element(*RiskPOCLocators.DELETE_MODAL_BUTTON).click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(RiskPOCLocators.DRUPAL_ALERT))
            notif = self.driver.find_element(*RiskPOCLocators.DRUPAL_ALERT).text
            print("Notification:", notif)

            if "successfully deleted" in notif:
                print("POC Deleted Successfully.")
            else:
                print("POC Deletion Failed:", notif)
        except Exception as e:
            print("POC Deletion Failed:", e)