from selenium.webdriver.common.by import By
#
class RiskCodingToolLocators:
    DELETE_BUTTON=(By.XPATH,"//span[@data-badge-caption='Delete']")
    DELETE_MODAL_INPUT=(By.XPATH,"//input[@id='task_delete_input']")
    DELETE_CONFIRM_BUTTON=(By.XPATH,"//div[@class='modal-footer']//a[@data-index='confirm']")
    CHARTCONTAINER = (By.XPATH, "//div[contains(@id,'chart_container')]")
    DOCUMENT_NAME=(By.XPATH, "//div[contains(@class,'tab-heading')]//child::a")
    ADDED_DX =(By.XPATH, "//SPAN[@CLASS='reviewer_chk material-icons green-text']/parent::div/parent::td/preceding-sibling::td[contains(@class,'dx_code_col')]/child::div/child::span[@class='td-row1 icd_code']/child::span/child::select" )
    ADDED_HCCS=(By.XPATH,"//SPAN[@CLASS='reviewer_chk material-icons green-text']/parent::div/parent::td/preceding-sibling::td[contains(@class,'hcc_code_col')]/child::div/child::span[@class='td-row2 hcc-evnt']/span[1]")
    NUMBER_ENCOUNTERS=(By.XPATH,"//li[contains(@class,'enc_li ')]")
    ENCOUNTER_PROVIDER=(By.XPATH,"//li[contains(@class,'enc_li ')]/child::div/child::span[@prov_name]")
    ENCOUNTER_DATE=(By.XPATH,"//li[contains(@class,'enc_li ')]/child::div/child::span[contains(@class,'encounter_date')]")
    NOTES_ICON=(By.XPATH,"//a[@class='reviewer_comment note-ind not_disable' and @style='pointer-events: all;']")
    NOTES_TEXT=(By.XPATH,"//div[@class='modal-content ']/child::div/child::div/child::div[2]/child::div[@class='clippable-content']")
    NOTES_CLOSE_MODAL = ( By.XPATH, "//div[@class='modal-header']/child::div[2]/child::i")

