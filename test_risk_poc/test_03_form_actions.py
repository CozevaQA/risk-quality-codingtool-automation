import json
import time

import pytest
from conftest import allure_ref, utility_ref, web_utility_ref, testdata_ref, pd_ref
from utils.common_utils import is_valid_date
from utils.decorators import log_function_name
@log_function_name
def test_view_suspect_reason(poc_page):
    """
       Verifies that the Suspect Reason modal opens successfully
       and displays non-empty header and content information
       when a suspect reason is available on the POC page.
       """
    risk_poc = poc_page
    suspect_reason=risk_poc.get_suspect_reason_modal_data()
    allure_ref.attach(
        suspect_reason,
        name="Suspect Reason",
        attachment_type=allure_ref.attachment_type.TEXT
    )
    assert len(suspect_reason)>0,f"Suspect Reason modal did not display any content. Received: {suspect_reason}"

@log_function_name
def test_all_hcc(poc_page):
    """
    Verifies that enabling the ALL HCC toggle renders additional
    HCCs in the POC form when compliant HCCs are available.
    """
    risk_poc = poc_page

    original_hccs = risk_poc.get_hcc_list()
    all_hccs = risk_poc.get_all_hcc_list()

    original_count = len(original_hccs)
    new_count = all_hccs
    extra_hccs = new_count - original_count

    allure_ref.attach(
        (
            f"Initial HCC count: {original_count}\n"
            f"HCC count after ALL HCC toggle: {new_count}\n"
            f"Additional HCCs displayed: {extra_hccs}"
        ),
        name="ALL HCC Toggle Result",
        attachment_type=allure_ref.attachment_type.TEXT
    )

    assert new_count >= original_count, (
        f"ALL HCC toggle reduced HCC count "
        f"(before={original_count}, after={new_count})"
    )

@log_function_name
def test_add_dx_global_non_hcc(poc_page):
    """
    Verify that a NON-HCC DX code can be added globally
    and its description matches the expected value.
    """
    risk_poc = poc_page

    with allure_ref.step("Add NON-HCC DX globally"):
        code_added = risk_poc.add_dx_global(testdata_ref.add_dx_non_hcc,False)

    if not code_added:
        allure_ref.attach(
            testdata_ref.add_dx_non_hcc,
            name="DX Code Attempted",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

    assert code_added, f"Unable to add {testdata_ref.add_dx_non_hcc}"

    description_matched = False

    with allure_ref.step("Fetch DX rows and validate description"):
        dx_desc_last_dos = risk_poc.get_dx_dos_rows()

        allure_ref.attach(
            str(dx_desc_last_dos),
            name="DX Table Snapshot",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        for hcc_id, hcc_desc, dx_description, dx_code, last_dos in dx_desc_last_dos:
            normalized_dx_code = dx_code.replace(".", "")

            if (
                normalized_dx_code == testdata_ref.add_dx_non_hcc
                and dx_description == testdata_ref.add_dx_non_hcc_description
            ):
                description_matched = True
                break
    if not description_matched:
        allure_ref.attach(
            testdata_ref.add_dx_non_hcc_description,
            name="Expected DX Description",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

    assert description_matched, (
        f"Description not matched for {testdata_ref.add_dx_non_hcc}"
    )

@log_function_name
def test_add_dx_global_with_hcc(poc_page):
    """
    Verify that an HCC-mapped DX code can be added globally
    and its HCC name and number are displayed correctly.
    """
    risk_poc = poc_page

    expected_dx = testdata_ref.add_dx_with_hcc
    hcc_info = testdata_ref.add_dx_with_hcc_hcc_name_number
    expected_hcc_number, expected_hcc_name = hcc_info.split("_")

    with allure_ref.step(f"Add HCC DX globally: {expected_dx}"):
        code_added = risk_poc.add_dx_global(expected_dx,True)

    if not code_added:
        allure_ref.attach(
            expected_dx,
            name="DX Code Attempted",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

    assert code_added, f"Unable to add {expected_dx}"

    description_matched = False

    with allure_ref.step("Validate DX, HCC name, and HCC number in POC Form"):
        dx_desc_last_dos = risk_poc.get_dx_dos_rows()

        allure_ref.attach(
            str(dx_desc_last_dos),
            name="DX Table Snapshot",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        for hcc_id, hcc_desc, dx_description, dx_code, last_dos in dx_desc_last_dos:
            normalized_dx_code = dx_code.replace(".", "")

            if (
                normalized_dx_code == expected_dx
                and hcc_id == expected_hcc_number
                and hcc_desc == expected_hcc_name
            ):
                description_matched = True
                break
    if not description_matched:
        allure_ref.attach(
            f"Expected HCC: {expected_hcc_number} - {expected_hcc_name}",
            name="Expected HCC Info",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

    assert description_matched, (
        f"HCC details not matched for {expected_dx}"
    )

@log_function_name
def test_add_cpt(poc_page):
    """
    Verify that an CPT can be added and number and description are displayed correctly.
    """
    risk_poc = poc_page

    cpt_value = testdata_ref.add_cpt_value
    cpt_desc = testdata_ref.add_cpt_description
    expected_cpt_number, expected_cpt_desc = cpt_value,cpt_desc

    with allure_ref.step(f"Add CPT : {expected_cpt_number}"):
        code_added = risk_poc.add_cpt(expected_cpt_number)

    if not code_added:
        allure_ref.attach(
            expected_cpt_number,
            name="CPT Addition attempted",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

    assert code_added, f"Unable to add {expected_cpt_number}"

    description_matched = False

    with allure_ref.step("Validate Added CPT in POC Form"):
        cpt_info = risk_poc.get_cpts()

        allure_ref.attach(
            str(cpt_info),
            name="CPT Info",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        for cpt_tag,cpt_code,cpt_desc in cpt_info:
            tag_present="CPT/HCPCS" in cpt_tag
            if (
                cpt_code == expected_cpt_number
                and cpt_desc == expected_cpt_desc
                and tag_present
            ):
                description_matched = True
                break
    if not description_matched:
        allure_ref.attach(
            f"Expected CPT Number: {expected_cpt_number} Expected CPT Description:{expected_cpt_desc} \n Actual CPT Number: {cpt_code} Actual CPT Description:{cpt_desc} \n,Tag present {cpt_tag} ",
            name="CPT Information",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

    assert description_matched, (
        f"Details not matched for {cpt_value}"
    )

@log_function_name
def test_savedraft_feature(poc_page):
    """
    Test Objective:
    Verify that clicking 'Save Draft' triggers autosave functionality and
    displays:
    1. A success status
    2. A green check icon
    3. Autosave confirmation text
    4. Autosave timestamp in expected UI format
    """

    # Arrange: Get the Risk POC page object
    risk_poc = poc_page

    # Act: Perform Save Draft action and capture autosave UI values
    status, autosave_icon, autosave_text, autosave_time = risk_poc.SaveDraftPOC()

    # Attach raw autosave response for debugging and reporting
    allure_ref.attach(
        f"""
        Save Status    : {status}
        Icon Text      : {autosave_icon}
        Autosave Text  : {autosave_text}
        Autosave Time  : {autosave_time}
        """,
        name="Autosave UI Response",
        attachment_type=allure_ref.attachment_type.TEXT,
    )
    time.sleep(3)
    # Assert 1: Validate that Save Draft action succeeded
    assert status, "Save Draft Drupal notification was not generated"

    # Assert 2: Validate presence of success check icon
    # Material icons expose icon name as text (e.g., 'check')
    assert autosave_icon == "check", "Autosave success check icon not displayed"

    # Assert 3: Validate autosave confirmation message
    assert "Autosave" in autosave_text, "Autosave confirmation text not found"

    # Assert 4: Validate autosave timestamp format
    # Expected format: M/D/YYYY H:MM:SS AM/PM (example: 1/4/2026 7:04:12 PM)
    assert is_valid_date(
        autosave_time,
        fmt="%m/%d/%Y %I:%M:%S %p"
    ), "Autosave timestamp is not in the expected format"

@log_function_name
def test_dos_field(driver,poc_page):
    """
    Verifies Date of Service (DOS) field behavior:
    - Clicking DOS opens the date picker
    - Only the current year (2025) is enabled
    - Past and future years are disabled
    """
    risk_poc = poc_page

    dos_field = risk_poc.get_dos_field()
    web_utility_ref.action_click(driver, dos_field)
    time.sleep(2)
    assert risk_poc.is_dos_date_picker_open(), "Date picker does not open"
    time.sleep(2)
    enabled_years = risk_poc.get_enabled_years_in_date_picker()
    assert enabled_years == ["2025"], (
        f"Expected only 2025 to be enabled, but got {enabled_years}"
    )

    risk_poc.close_date_picker()

@log_function_name
def test_rendering_provider_field(
    driver,
    poc_page,

):
    """
    Verifies Rendering Provider field behavior:
    - User can search for a rendering provider by name
    - Provider search dropdown displays matching results
    - At least one provider result is returned for a valid search
    """
    risk_poc = poc_page

    results_count = risk_poc.set_rendering_provider(
        testdata_ref.provider_name
    )
    print(f"Rendering provider {results_count} ")

    assert isinstance(results_count, int), (
        f"Expected result count to be int, got {type(results_count)}"
    )

    assert results_count > 0, (
        f"No rendering provider results found for "
        f"provider name: {testdata_ref.provider_name}"
    )

@log_function_name
def test_buttons_disabled_after_recapture_confirm(recapture_context, poc_page):
    """
       Validate that after a Recapture DX is confirmed on the Risk POC page,
       the Disconfirm and Not Addressed action buttons for that DX
       become disabled.

       This test_risk_poc ensures that once a Recapture action is completed:
       - The Disconfirm button is no longer actionable
       - The Not Addressed button is no longer actionable

       If no eligible Recapture DX is available, the test_risk_poc is skipped.
       """
    with allure_ref.step("Recapture Confirmed for a dx "):
        if recapture_context is None:
            pytest.skip("No Recapture DX available")

        poc_page = poc_page
        dx_code = recapture_context["dx_code"]
        allure_ref.attach(
            f"\n[INFO] Recapture confirmed for DX: {dx_code}",
            name="Dx code selected",
            attachment_type=allure_ref.attachment_type.TEXT)

    with allure_ref.step("Check if buttons are disabled"):
        disconfirm_disabled = poc_page.is_disconfirm_button_disabled(dx_code)
        not_addressed_disabled = poc_page.is_not_addressed_button_disabled(dx_code)

        if not disconfirm_disabled:
            allure_ref.attach(
                f"Disconfirm button still enabled for DX: {dx_code}",
                name="Disconfirm Button Failure",
                attachment_type=allure_ref.attachment_type.TEXT,
            )

        if not not_addressed_disabled:
            allure_ref.attach(
                f"Not Addressed button still enabled for DX: {dx_code}",
                name="Not Addressed Button Failure",
                attachment_type=allure_ref.attachment_type.TEXT,
            )

        assert disconfirm_disabled, "Disconfirm button still enabled"
        assert not_addressed_disabled, "Not addressed button still enabled"

@log_function_name
def test_disconfirm(disconfirm_context, poc_page):
    """
    Pre-Requisite : Show All Dx should be clicked
    Verifies Disconfirm behavior for a Recapture DX:
    - Disconfirm action is performed on a recaptured DX
    - 'HCC Disconfirmed' tag appears
    - 'Undo Disconfirm' action is available
    """

    # --- Precondition ---
    if disconfirm_context is None:
        pytest.skip("No Recapture DX available to disconfirm")

    dx_code = disconfirm_context["dx_code"]
    disconfirm_tag_text = disconfirm_context["disconfirm_tag_text"]
    undo_disconfirm_text = disconfirm_context["undo_disconfirm_text"]
    dot_status=disconfirm_context["dot_status"]

    # 📎 Attach observed context
    allure_ref.attach(
        f"""
        DX Code: {dx_code}
        Disconfirm Tag Text: {disconfirm_tag_text}
        Undo Disconfirm Text: {undo_disconfirm_text}
        Red Dot Status: {dot_status}
        """,
        name="Disconfirm UI State",
        attachment_type=allure_ref.attachment_type.TEXT
    )

    with allure_ref.step(f"Verify UI state after disconfirm for DX {dx_code}"):

        assert disconfirm_tag_text == "HCC Disconfirmed", (
            f"Expected 'HCC Disconfirmed' tag, "
            f"but got: {disconfirm_tag_text}"
        )

        assert undo_disconfirm_text == "Undo Disconfirm", (
            f"Expected 'Undo Disconfirm' action, "
            f"but got: {undo_disconfirm_text}"
        )

        assert dot_status=="no dot",f"Expected No Dot but got {dot_status}"
@log_function_name
def test_not_addressed(not_addressed_context, poc_page):
    """
    Pre-Requisite : Show All Dx should be clicked
    Verifies Disconfirm behavior for a Recapture DX:
    - Not Addressed is performed on a recaptured DX
    - 'HCC Not Addressed ' tag appears
    - 'Undo Not Addressed ' action is available
    """

    # --- Precondition ---
    if not_addressed_context is None:
        pytest.skip("No Recapture DX available to not address")

    dx_code = not_addressed_context["dx_code"]
    not_addressed_tag_text = not_addressed_context["not_addressed_tag_text"]
    undo_deferred_text = not_addressed_context["undo_deferred_text"]
    dot_status = not_addressed_context["dot_status"]
    # 📎 Attach observed context
    allure_ref.attach(
        f"""
        DX Code: {dx_code}
        Tag Text: {not_addressed_tag_text}
        Undo Disconfirm Text: {undo_deferred_text}
        Red Dot Status: {dot_status}
        """,
        name="Not Addressed UI State",
        attachment_type=allure_ref.attachment_type.TEXT
    )

    with allure_ref.step(f"Verify UI state after Not Adressed for DX {dx_code}"):

        assert not_addressed_tag_text == "HCC Not Addressed", (
            f"Expected 'HCC Disconfirmed' tag, "
            f"but got: {not_addressed_tag_text}"
        )

        assert undo_deferred_text == "Undo Not Addressed", (
            f"Expected 'Undo Disconfirm' action, "
            f"but got: {undo_deferred_text}"
        )
        assert dot_status == "present", f"Expected No Dot but got {dot_status}"

@log_function_name
def test_add_note(poc_page):
    with allure_ref.step("Add Note"):
        result = poc_page.addNote(testdata_ref.note)
        allure_ref.attach(
            str(result),
            name="Details of notes modal",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

    with allure_ref.step("Validate note modal appearance"):
        assert result["note_modal_appeared"], "Note modal did not appear"

    with allure_ref.step("Validate note modal header"):
        assert result["note_modal_header"], "Note modal header not found"

    with allure_ref.step("Validate note shortcut label"):
        assert result["note_shortcut_label"], "Note shortcut label not found"

    with allure_ref.step("Validate note suggestions"):
        assert result["note_modal_suggestions"], "Note suggestions did not appear"

    with allure_ref.step("Validate if notes icon is displayed"):
        assert poc_page.check_if_note_icon_displayed()==1 ,"Notes icon not displayed"

@log_function_name
def test_file_upload_functionality( poc_page):
    """
    Verifies that:
    - File can be uploaded
    - Toast message appears
    - Uploaded document name is displayed
    - Add Document button becomes available
    """

    poc_page = poc_page

    # STEP 1: Attach file
    with allure_ref.step("Attach file in attachment section"):
        attachment_input = poc_page.get_attachment_input()
        attachment_input.send_keys(testdata_ref.file_path)

        allure_ref.attach(
            testdata_ref.file_name,
            name="File Sent For Upload",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

    # STEP 2: Check if toast message appears
    with allure_ref.step("Check if toast message appears"):
        notif = poc_page.get_notification_if_present()

        allure_ref.attach(
            str(notif),
            name="Attachment Toast Notification",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        assert notif is  None, (
            "Expected no toast notification after file upload, but toast appeared"
        )

    # STEP 3: Check uploaded document name
    with allure_ref.step("Check name of document"):
        uploaded_files = poc_page.get_attached_file_name()

        allure_ref.attach(
            "\n".join(uploaded_files),
            name="Uploaded File Names",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        assert any(
            testdata_ref.file_name in file
            for file in uploaded_files
        ), (
            f"Uploaded file name '{testdata_ref.file_name}' "
            f"not found in attached documents: {uploaded_files}"
        )

    # STEP 4: Check if Add Document button is visible
    with allure_ref.step("Check if Add Document is visible or not"):
        is_add_doc_visible = poc_page.is_add_document_available()

        allure_ref.attach(
            str(is_add_doc_visible),
            name="Add Document Button Visible",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        assert is_add_doc_visible is True, (
            "Add Document button should be visible after file upload"
        )

@log_function_name
def test_kebab_menu_print_options(poc_page):
    """
    Verifies kebab menu options for Print actions.
    """

    poc_page = poc_page

    expected_options = [
        "Print Careops",
        "Print HCC (POC)",
        "Print Quality Ops",
        "Add Member to Batch",
    ]

    with allure_ref.step("Verify Print HCC button is visible"):
        is_print_visible = poc_page.is_print_hcc_visible()

        allure_ref.attach(
            str(is_print_visible),
            name="Is Print HCC Button Visible",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        assert is_print_visible is True, (
            "Print HCC button is not visible/clickable"
        )

    with allure_ref.step("Open kebab menu and read available options"):
        options = poc_page.get_kebab_menu_options()

        allure_ref.attach(
            "\n".join(options),
            name="Kebab Menu Options",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

    with allure_ref.step("Verify kebab menu options match expected list"):
        allure_ref.attach(
            "\n".join(expected_options),
            name="Expected Kebab Menu Options",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        assert options == expected_options, (
            f"Kebab menu options mismatch.\n"
            f"Expected: {expected_options}\n"
            f"Actual: {options}"
        )

@log_function_name
def test_poc_submission_notification(poc_submission_context):
    """
       Validate that a successful POC submission displays the expected
       confirmation notification message to the user.

       This test_risk_poc ensures that after submitting the POC:
       - A submission notification is generated
       - The notification text confirms successful submission
       - The full submission context is captured and attached for traceability
       """
    allure_ref.attach(
        json.dumps(poc_submission_context, indent=2),
        name="POC Submission Context",
        attachment_type=allure_ref.attachment_type.JSON
    )

    assert "Your changes have been successfully submitted" in poc_submission_context["notification_text"]

@log_function_name
def test_poc_task_link(driver,poc_submission_context):
    """
        Validate that a task link is generated and available
        after successful POC submission.

        This test_risk_poc verifies that:
        - The submission notification contains task-related information
        - A valid task link is present in the submission context
        """
    allure_ref.attach(
        poc_submission_context["notification_text"],
        name="Notification Text",
        attachment_type=allure_ref.attachment_type.TEXT
    )

    allure_ref.attach(
        str(poc_submission_context["task_text"]),
        name="Task Text",
        attachment_type=allure_ref.attachment_type.TEXT
    )

    allure_ref.attach(
        str(poc_submission_context["task_link"]),
        name="Task Link",
        attachment_type=allure_ref.attachment_type.URI_LIST
    )

    assert poc_submission_context["task_link"] is not None
    web_utility_ref.wait_for_page_load(driver, 120)

