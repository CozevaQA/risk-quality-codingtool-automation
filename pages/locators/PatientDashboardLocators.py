# pages/locators/patient_dashboard_locators.py
from selenium.webdriver.common.by import By

class PatientDashboardLocators:
    HCC_TABLE = (By.XPATH, '//div[@id="hcc_measures"]')
    NON_COMPLIANT_DX = (By.XPATH, '//div[@class="poc_dashboard pbb"]//child::div[@prev_status="red_dot"]//following-sibling::div[@class="clear dx_detail"]//child::div[contains(@class,"dx_row current_yr")]')
    FIRST_PENCIL_ICON = (By.XPATH, '(//div[@class="poc_dashboard pbb"]//child::i)[1]')
    OPEN_POC_BUTTON = (By.XPATH, '(//a[text()="Confirm/Disconfirm"])[1]')
    DX_CODES = (By.XPATH, '//div[@class="code_details col careops-new"]')
    HCC_RED_DOTS=(By.XPATH,'//div[@class="poc_dashboard pbb"]//child::div[@prev_status="red_dot"]')
    HIDE_BANNER=(By.XPATH , "//div[@class='banner_footer']//child::a[contains(text(),'Hide')]")
    STALE_ROW=(By.XPATH,"//span[contains(@class,'stale') and not(contains(@class,'hide'))]")
    HCC_ROW=(By.XPATH,"//div[contains(@class,'clear hcc_row')]")
    STALE_ICON=(By.XPATH,"//div[contains(@class,'stale')]")
    DX_CODES_HCC=(By.XPATH,"//div[contains(@class,'dx_detail')]//child::div[contains(@class,'dx_row')]")
    HCC_DOT_STATUS=(By.XPATH,".//div[contains(@class,'dot')]")
    FIRST_DROPDOWN_XPATH=(By.XPATH,"//span[@class='material-icons' and text()='arrow_drop_down']")
    SECOND_DROPDOWN_XPATH=(By.XPATH,"(//i[text()='chevron_right'])[3]")
    DOCUMENTS_LINK=(By.XPATH,"(//ul[@class='patient_submenu'])[2]//*[text()='Documents']")
    DOCUMENTS=(By.XPATH,"//tr[@role='row']//div[@class='patient_document_name']")
    STALE_HCC_MEASURES=(By.XPATH,"//div[@class='pls stale material-icons prs grey-text text-darken-1 upd ']/ancestor::div[contains(@class,'hcc_row')]")
    HOLLOW_DOT_HCCS=(By.XPATH,"//div[contains(@class,'hollow_red')]/parent::div")
    NO_DOT_HCCS=(By.XPATH,"//div[contains(@class,'no_dot')]/parent::div")

