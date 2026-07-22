from selenium.webdriver.common.by import By

class RiskPOCLocators:

    # -------------------- Existing Locators --------------------
    POC_DX = (
        By.XPATH,
        '//div[@class="dx_code_div gray_background"]//child::div'
    )

    SHOW_DX_BUTTON = (
        By.XPATH,
        '//div[@class="collapse flex"]//child::span[2]'
    )

    RISK_LABEL = (By.XPATH, "//div[@class='risk_header']")
    RISK_COUNT = (By.XPATH, "//span[@class='risk_count']")

    # -------------------- Dashboard / Structure --------------------
    DASHBOARD = (By.XPATH, "//*[@class='poc_dashboard pbb']")
    POC_BODY = (By.XPATH, "//*[@class='poc_body']")

    # -------------------- Buttons / Actions --------------------
    CONFIRM_DISCONFIRM = (By.XPATH, "//*[contains(text(),'Confirm/Disconfirm')]")
    PRE_REVIEW_REPORT = (By.XPATH, "//*[contains(text(),'Pre-review Report')]")

    # -------------------- Tags --------------------
    RECAPTURE_TAG = (By.XPATH, "//span[contains(text(),'Recapture')]")
    SUSPECT_TAG = (By.XPATH, "//span[contains(text(),'Suspect')]")



    # -------------------- Tooltips (Placeholders – Add real XPaths later) --------------------
    CONFIRM_TOOLTIP = None
    DISCONFIRM_TOOLTIP = None
    NOT_ADDRESSED_TOOLTIP = None
    SUSPECT_REASON = (
        By.XPATH,
        "//span[contains(@class,'suspect_anchor')]"
    )
    SUSPECT_REASON_MODAL=(By.XPATH,"//div[@class='modal cozeva-prompt poc_modal open']")
    SUSPECT_REASON_MODAL_CONTENT = (By.XPATH ,"//div[@class='modal-content ']")
    SUSPECT_REASON_HEADER_CONTENT = (By.XPATH, "//div[@class='modal-header-content']")
    SUSPECT_REASON_MODAL_CLOSE=(By.XPATH, "//div[@class='modal cozeva-prompt poc_modal open']//child::i[text()='clear']")

    # -------------------- Add DX Modal --------------------
    ADD_DX_BUTTON = (By.XPATH , "//div[@class='poc_header row']//div[contains(text(),'+ Add Dx')]")
    ADD_CPT_BUTTON = (By.XPATH, "//div[@class='flex']//div[contains(text(),'+ Add CPT')]")
    ADD_DX_MODAL_INPUT = (By.XPATH, "//div[@class='modal-content ']//child::input[@id='dx_search_input']")
    ADD_CPT_MODAL_INPUT = (By.XPATH, "//div[@class='modal-content ']//child::input[@id='cpt_search_input']")
    ADD_DX_MODAL_LIST = (By.ID, "ac-dropdown-review_dx_input")
    ADD_CPT_MODAL_LIST = (By.ID, "ac-dropdown-cpt_search_input")
    DX_SEARCH_RESULTS=(By.XPATH,"//ul[@id='ac-dropdown-dx_search_input']//child::div[@class='hcc_search']")
    DX_SEARCH_NOT_FOUND=(By.XPATH , "//li[@class='no_sug']")
    CPT_SEARCH_RESULTS=(By.XPATH,"//ul[@id='ac-dropdown-cpt_search_input']//child::li//div")
    DX_CLOSE_MODAL=(By.XPATH ,"//div[@class='modal-header']//child::i[contains(text(),'clear')]" )






    # -------------------- Notes Section --------------------
    ADD_NOTE_BUTTON = (By.XPATH,"(//div[@class='clear dx_detail'])[1]//child::div[contains(@class,'action_boxes')]//child::i[contains(text(),'vert')]")                    # TODO: update when you get locator
    NOTE_TEXTAREA = (By.XPATH, "//textarea[@id='edit-note-field']")
    NOTE_SAVE_BUTTON = (By.XPATH, "//div[@class='modal-footer']//a")
    NOTE_SUGGESTIONS_LIST = (By.XPATH, "//ul[@id='ac-dropdown-edit-note-field']")
    NOTE_HEADER=(By.XPATH , "//div[@class='modal-header-content']")
    NOTE_SHORTCUT_LABEL=(By.XPATH,"//span[@class='helper-text orange-text right']")
    VISIBLE_NOTES=(By.XPATH,"//a[@data-note and normalize-space(@data-note)!='']")

    # -------------------- DOS / Provider Fields --------------------
    DOS_FIELD = (By.ID, "enc_service_date")
    PROVIDER_FIELD = (By.ID, "provider_name")
    PROVIDER_LIST = (By.XPATH, "//ul[@id='ac-dropdown-provider_name']")

    CONFIRM_MODAL = (By.XPATH ," //div[@class= 'modal-header-content' and text()='Confirm']")
    CONFIRM_MODAL_SUBMIT = (By.XPATH ,"//div[@class='modal-footer']//child::a[@data-index='confirm']")
    DOS_DATE=(By.XPATH,"//input[@name='service-date']")
    DATE_PICKER= (By.CLASS_NAME, "cmp-date-time-picker")
    VISIBLE_YEAR_DATEPICKER=(By.XPATH,"//span[@class='cmp-dp-txt J-dtp-year-txt']")
    ENABLED_YEAR_DATEPICKER=(By.XPATH,"//span[@class='cmp-dp-year-item J-dtp-year-item']")
    FOOTER=(By.XPATH,"//div[@class='poc_footer poc_footer_normal']")
    CURRENT_DAY=(By.XPATH,".//*[contains(@class,'cmp-dp-date-item-cur') ]")

    RENDERING_PROVIDER=(By.XPATH,"//input[@name='provider-search']")
    RENDERING_PROVIDER_SEARCH_RESULTS=(By.XPATH,".//*[contains(@id,'ac-dropdown-provider_name')]//li")
    RENDERING_PROVIDER_SEARCH_RESULT=(By.XPATH,"(.//*[contains(@id,'ac-dropdown-provider_name')]//li//div/text()[1])[1]")

    # ------------------ ALL HCC -------------------------------
    ALL_HCCS_TOGGLE= (By.XPATH , "//input[@onchange='poc_toggle();']//ancestor::label//child::span")
    AUTOSAVE_ICON = (By.XPATH,"//div[contains(@class , 'last_draft_time_div mrm')]//child::i[contains(@class ,'tiny material-icons valign-m green-text' )]")
    AUTOSAVE_TEXT = (By.XPATH,"//div[contains(@class , 'last_draft_time_div mrm')]")
    AUTOSAVE_TIME = (By.XPATH,"//div[contains(@class , 'last_draft_time_div mrm')]//child::span[contains(@id,'last_draft_time' )]")

    CONFIRMED_DX_CHECKBOX= (By.XPATH,"//div[contains(@class,'action_box tick_box tooltipped mrs selected')]")
    VISIBLE_HCC_DISCONFIRM=(By.XPATH,"//span[@class='btn_title' and contains(text(), 'HCC Disconfirmed') ]//ancestor::div[contains(@class,'disconfirm_tag') and not(contains(@class,'hide'))]")
    VISIBLE_HCC_NOT_ADDRESSED=(By.XPATH,"//span[@class='btn_title' and contains(text(), 'HCC Not Addressed') ]//ancestor::div[contains(@class,'deferred_tag ') and not(contains(@class,'hide'))]")
    PARENT_HCC_ROW=(By.XPATH,".//ancestor::div[contains(@class,'hcc_row ')]")
    #----------------------CORE ELEMENTS------------------------------

    DOS_LABEL = (By.XPATH ,"//label[contains(text(),'Date of Service')]")
    CURRENT_DATE=(By.XPATH,"//span[@class='cmp-dp-date-item cmp-dp-date-item-cur J-dtp-date-item']")

    SERVICE_YEAR_DROPDOWN=(By.XPATH ,"//div[@class='year_header']//child::input[@id='select-meas-year-materialize-dropdown-input']")
    ADD_DX_BUTTON = (By.XPATH ,"//div[@class='dx_search poc_btn col mtm mln' and contains(text(),'+ Add Dx')]")
    ALL_HCCS_TOGGLE = (By.XPATH ,"//span[@class='dashboard_toggle switch mr-right-event mt-15']")
    ALL_HCCS_LABEL = (By.XPATH ,"//span[@class='poc_all_hcc']" )
    QUALITY_BUTTON = (By.XPATH,"//div[@class='col second_col w38p allview_quality_wrapper mtm poc_btn_style back_btn_poc right' ]")
    ADD_CPT_LINK = (By.XPATH,"//div[@class='cpt_search flex link_color lma rfloat cursor_pointer mrb' ]")
    SWITCH_TO_OLD_VIEW_LINK = (By.XPATH,"//div[@class='poc_toggle flex link_color cursor_pointer mrb' ]")
    RENDERING_PROVIDER_FIELD = (
        By.XPATH,
        "//input[@id='provider_name']"
    )

    RENDERING_PROVIDER_LABEL = (
        By.XPATH,
        "//label[contains(text(),'Rendering Provider')]"
    )

    SAVE_DRAFT_BUTTON = (
        By.XPATH,
        "//div[@id='save_draft' and contains(text(),'Save Draft')]"
    )

    SUBMIT_BUTTON = (
        By.XPATH,
        "//div[@id='poc-submit' and contains(@class,'poc_submit_btn')]"
    )

    ATTACHMENT_HEADER=(By.XPATH,"//span//child::b[text()='Attachments']")

    # is_displayed will be false for this in the UI
    ATTACHMENT_SECTION_FILE = (By.XPATH, "//div[@class='fixed_right_panel']//input[contains(@class, 'file_upload_attachment') and @type='file']")


    ATTACHMENT_SECTION_PATIENT_DOCUMENTS = (
        By.XPATH,
        "//a//child::b[text()='Patient Documents']"
    )
    ATTACHMENT_SECTION_CSG = (
        By.XPATH,
        "//a//child::span[contains(text(),'Cozeva Secure Gateway')]"
    )
    PRINT_BUTTON=(By.XPATH,"//img[@alt='Print Icon']")
    KEBAB_MENU_ICON=(By.XPATH ,"//img[@alt='Patient Print Options']")
    KEBAB_MENU_OPTIONS=(By.XPATH,"//ul[@id='patient_print_dropdown']//child::li//a")
    ATTACHED_FILE_NAMES=(By.XPATH,"//div[@class='fixed_right_panel']//div[contains(@class, 'row thumbnail_preview') ]//child::li[@class='tab']//a")
    ADD_DOCUMENT_BUTTON=(By.XPATH,"//ul[contains(@id,'right_panel_nav_tabs')] //div[contains(text(), 'Add Document')]")
    DISCLAIMER_LINK=(By.XPATH, "//div[@id='poc_disclaimer']//span[text()='see more']")

    # ------------------------------ POC Body -----------------------------

    DISPLAYED_HCCS=(By.XPATH,"//div[contains(@class,'clear hcc_row plm') and not(contains(@class, 'hide'))]")
    HCC_HIERARCHIES = (By.CLASS_NAME ,'groupped_hcc_banner')
    ALL_DX=(By.XPATH,"//div[@class='dx_code_div gray_background']")
    DISPLAYED_CPT=(By.XPATH,"//div[contains(@id,'cpt') and not(contains(@class, 'hide'))]")
    CPT_TAG=(By.XPATH,"//div[contains(@id,'cpt') and not(contains(@class, 'hide'))]//child::span[contains(@class,'tag-block')]")
    CPT_ROWS=(By.XPATH,"//div[contains(@id,'cpt') and not(contains(@class, 'hide'))]//child::div[@class='clear cpt_detail']//child::div[contains(@class,'cpt_row')]")
    CPT_CODE=(By.CSS_SELECTOR,".col.cpt_description")
    CPT_DESCRIPTION=(By.CSS_SELECTOR,".dx_code_div.gray_background")
    # -------------------- POC Primary Buttons --------------------
    SAVE_DRAFT = (By.ID, "save_draft")
    SUBMIT = (By.ID, "poc_submit")
    DELETE = (By.ID, "delete_task")

    # -------------------- Alerts / Messages --------------------
    DRUPAL_ALERT = (By.XPATH, "//*[@class='drupal_message_text']")
    AUTOSAVE_STATUS = (By.ID, "last_draft_time")

    # -------------------- Delete Modal --------------------
    DELETE_REASON_INPUT = (
        By.XPATH,
        "//*[contains(text(),'Are you sure you want to delete this task?')]/..//*[@class='input-field']"
    )

    DELETE_MODAL_BUTTON = (
        By.XPATH,
        "//*[contains(text(),'Delete')]"
    )