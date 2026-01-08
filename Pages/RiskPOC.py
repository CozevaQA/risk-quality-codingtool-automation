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

    def RecaptureConfirm(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            self.driver.find_element(By.XPATH, loc.recapture_tag_xpath).finfd_element(By.XPATH, loc.confirm_tooltip_xpath).click()
            print("Recapture Confirmed Successfully.")
        except exceptions as e:
            print("Recapture Confirm Failed: ", e)
    
    def RecaptureDisconfirm(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            self.driver.find_element(By.XPATH, loc.recapture_tag_xpath).find_element(By.XPATH, loc.disconfirm_tooltip_xpath).click()
            print("Recapture Disconfirmed Successfully.")
        except exceptions as e:
            print("Recapture Disconfirm Failed: ", e)

    def RecaptureNotAddressed(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            self.driver.find_element(By.XPATH, loc.recapture_tag_xpath).find_element(By.XPATH, loc.not_addressed_tooltip_xpath).click()
            print("Recapture Marked as Not Addressed Successfully.")
        except exceptions as e:
            print("Recapture Not Addressed Failed: ", e)

    def SuspectConfirm(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            self.driver.find_element(By.XPATH, loc.suspect_tag_xpath).find_element(By.XPATH, loc.confirm_tooltip_xpath).click()
            print("Suspect Confirmed Successfully.")
        except exceptions as e:
            print("Suspect Confirm Failed: ", e)

    def SuspectDisconfirm(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            self.driver.find_element(By.XPATH, loc.suspect_tag_xpath).find_element(By.XPATH, loc.disconfirm_tooltip_xpath).click()
            print("Suspect Disconfirmed Successfully.")
        except exceptions as e:
            print("Suspect Disconfirm Failed: ", e)

    def SuspectNotAddressed(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            self.driver.find_element(By.XPATH, loc.suspect_tag_xpath).find_element(By.XPATH, loc.not_addressed_tooltip_xpath).click()
            print("Suspect Marked as Not Addressed Successfully.")
        except exceptions as e:
            print("Suspect Not Addressed Failed: ", e)

    def AddDiagnosis(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            self.driver.find_element(By.XPATH, loc.add_dx_btn_xpath).click()
            print("Add Diagnosis Button Clicked Successfully.")
            self.driver.find_element(By.ID, loc.add_dx_modal_id).send_keys(data.dx_code)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, loc.add_dx_modal_list_id)))
            self.driver.find_element(By.ID, loc.add_dx_modal_list_id).find_elements(By.TAG_NAME, "li")[1].click()
            print("Diagnosis Added Successfully.")
        except exceptions as e:
            print("Add Diagnosis Failed: ", e)

    def AddNote(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            self.driver.find_element(By.XPATH, loc.add_note_xpath).click()
            print("Add Note Button Clicked Successfully.")
            self.driver.find_element(By.ID, loc.note_text_id).send_keys(data.note)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.note_suggestions_list_xpath)))
            self.driver.find_element(By.XPATH, loc.note_suggestions_list_xpath).find_elements(By.TAG_NAME, "li")[1].click()
            self.driver.find_element(By.XPATH, loc.note_save_btn_xpath).click()
            print("Note Added Successfully.")
        except exceptions as e:
            print("Add Note Failed: ", e)
    
    def SetDOS(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            dos_field = self.driver.find_element(By.ID, loc.dos_field_id)
            dos_field.clear()
            dos_field.send_keys(data.dos_field)
            print("Date of Service Set Successfully.")
        except exceptions as e:
            print("Set Date of Service Failed: ", e)
    
    def SetProvider(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            provider_field = self.driver.find_element(By.XPATH, loc.provider_field_xpath)
            provider_field.clear()
            provider_field.send_keys(data.provider_name)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.provider_list_xpath)))
            self.driver.find_element(By.XPATH, loc.provider_list_xpath).find_elements(By.TAG_NAME, "li")[1].click()
            print("Provider Set Successfully.")
        except exceptions as e:
            print("Set Provider Failed: ", e)

    def SaveDraftPOC(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            self.driver.find_element(By.ID, loc.poc_save_draft_btn_id).click()
            notif = self.driver.find_element(By.ID, loc.drupal_alert_class_xpath).text
            print("Notification: ", notif)
            if "changes have been successfully saved" in notif:
                time = self.driver.find_element(By.ID, loc.autosave_id).text
                print("Autosave Time Updated Successfully: ", time)
            else:
                print("Draft Save Failed: ", notif)
            print("POC Draft Saved Successfully.")
        except exceptions as e:
            print("POC Draft Save Failed: ", e)
    
    def SubmitPOC(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            self.driver.find_element(By.ID, loc.poc_submit_btn_id).click()
            notif = self.driver.find_element(By.ID, loc.drupal_alert_class_xpath).text
            print("Notification: ", notif)
            if "has been created" in notif:
                print("POC Submitted Successfully.")
            else:
                print("POC Submission Failed: ", notif)
        except exceptions as e:
            print("POC Submission Failed: ", e)

    def DeletePOC(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.poc_body_xpath)))
            self.driver.find_element(By.ID, loc.poc_delete_btn_id).click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, loc.delete_reason_input_xpath)))
            self.driver.find_element(By.XPATH, loc.delete_reason_input_xpath).send_keys(data.delete_reason)
            self.driver.find_element(By.XPATH, loc.delete_modal_btn_xpath).click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, loc.drupal_alert_class_xpath)))
            notif = self.driver.find_element(By.ID, loc.drupal_alert_class_xpath).text
            print("Notification: ", notif)
            if "successfully deleted" in notif:
                print("POC Deleted Successfully.")
            else:
                print("POC Deletion Failed: ", notif)
        except exceptions as e:
            print("POC Deletion Failed: ", e)