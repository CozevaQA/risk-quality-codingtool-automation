import json
import re

import pytest

from pages.PatientDashboard import Patient_Dashboard
from utils.notifications import notify_success
from pages.RiskCodingTool import RiskCodingTool
from testresource import environment
from conftest import allure_ref, utility_ref, web_utility_ref, testdata_ref, pd_ref
from utils.decorators import log_function_name
from conftest import allure_ref, utility_ref, web_utility_ref, testdata_ref, pd_ref

@log_function_name
def test_document_displayed(driver, poc_submission_context, coding_tool_page):
    """Verifies whether document name is displayed correctly and document panel shows up"""

    document_status = coding_tool_page.get_document_attached()

    allure_ref.attach(
        str(document_status),
        name="Document Status",
        attachment_type=allure_ref.attachment_type.TEXT
    )

    assert document_status[0] == testdata_ref.file_name, \
        f"Expected {testdata_ref.file_name}, got {document_status[0]}"

    assert document_status[1], "Document is not displayed correctly"

@log_function_name
def test_submitted_dx(driver, poc_submission_context, coding_tool_page):
    print("Checking submitted Dx")
    confirmed_dx = poc_submission_context["confirmed_dxs"]
    with allure_ref.step("Collect Dx from coding tool"):
        dx_codes_codingtool = coding_tool_page.get_dx_submitted()

        allure_ref.attach(
            str(dx_codes_codingtool),
            name="Collected Dx from coding tool",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        assert dx_codes_codingtool, "No DX Code found in coding tool"

    with allure_ref.step("Validate if confirmed dx are in coding tool"):
        # ✅ Assert all confirmed HCCs exist in processed HCC list
        missing_hccs = set(confirmed_dx) - set(dx_codes_codingtool)

        assert not missing_hccs, (
            f"These confirmed HCCs are missing from dashboard: {missing_hccs}"
        )

        combined_data = {
            "Submitted DX in POC": confirmed_dx,
            "Submitted DX in coding tool": dx_codes_codingtool,
        }

        allure_ref.attach(
            json.dumps(combined_data, indent=2),
            name="Dashboard Data",
            attachment_type=allure_ref.attachment_type.JSON,
        )
@log_function_name
def test_submitted_hcc(driver, poc_submission_context, coding_tool_page):
    print("Checking submitted HCC")
    submitted_hccs = poc_submission_context["disconfirmed_hccs"] +poc_submission_context["confirmed_hccs"]
    print(submitted_hccs)
    with allure_ref.step("Collect HCC from coding tool"):
        hcc_codes_codingtool = coding_tool_page.get_hcc_submitted()
        print(hcc_codes_codingtool)
        allure_ref.attach(
            str(hcc_codes_codingtool),
            name="Collected HCC from coding tool",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        assert hcc_codes_codingtool, "No HCC found in coding tool"

    with allure_ref.step("Validate if submitted HCCs are in coding tool"):
        # ✅ Assert all confirmed and disconfirmed HCCs exist in processed HCC list
        missing_hccs = set(submitted_hccs) -set(hcc_codes_codingtool)

        assert not missing_hccs, (
            f"These confirmed HCCs are missing from dashboard: {submitted_hccs}"
        )

        combined_data = {
            "Submitted HCC in POC": submitted_hccs,
            "Submitted HCC in coding tool": hcc_codes_codingtool,
        }

        allure_ref.attach(
            json.dumps(combined_data, indent=2),
            name="Dashboard Data",
            attachment_type=allure_ref.attachment_type.JSON,
        )
#

@log_function_name
def test_encounter_info(
    driver,
    poc_submission_context,
    coding_tool_page,
):

    print("Checking encounter info")

    # Extract expected values from submission context
    expected_date = poc_submission_context["date_of_service"]

    full_provider_string = poc_submission_context["rendering_provider"]

    # Take only text before first bracket
    expected_provider = full_provider_string.split("(")[0].strip()

    print("Expected Provider:", expected_provider)
    print("Expected Date:", expected_date)

    with allure_ref.step("Collect encounter info from coding tool"):
        number_of_encounters, providers, dates = coding_tool_page.get_encounter_info()

        allure_ref.attach(
            str(providers),
            name="Providers from coding tool",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        allure_ref.attach(
            str(dates),
            name="Dates from coding tool",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

    assert number_of_encounters > 0, "No encounters found in coding tool"

    with allure_ref.step("Validate encounter provider and date"):

        # Check provider exists
        assert expected_provider in providers[0], (
            f"Expected provider '{expected_provider}' not found in coding tool providers {providers[0]}"
        )

        # Check date exists
        assert expected_date in dates, (
            f"Expected date '{expected_date}' not found in coding tool dates {dates}"
        )

        combined_data = {
            "Expected Provider": expected_provider,
            "Expected Date": expected_date,
            "Providers in Coding Tool": providers,
            "Dates in Coding Tool": dates,
        }

        allure_ref.attach(
            json.dumps(combined_data, indent=2),
            name="Encounter Validation Data",
            attachment_type=allure_ref.attachment_type.JSON,
        )

# def test_added_note(driver, poc_submission_context, coding_tool_page):

@log_function_name
def test_notes_info(
    driver,
    coding_tool_page,
):

    print("Checking notes info")

    expected_note = testdata_ref.note.strip()

    print("Expected Note:", expected_note)

    with allure_ref.step("Collect notes from coding tool"):
        number_of_notes, notes_texts = coding_tool_page.get_notes_info()

        allure_ref.attach(
            str(notes_texts),
            name="Collected Notes from coding tool",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

    assert number_of_notes > 0, "No notes found in coding tool"

    with allure_ref.step("Validate expected note exists in coding tool"):

        # If multiple notes exist, check expected note is present
        matching_notes = [
            note for note in notes_texts
            if expected_note in note
        ]

        assert matching_notes, (
            f"Expected note '{expected_note}' not found in coding tool notes {notes_texts}"
        )

        combined_data = {
            "Expected Note": expected_note,
            "Notes in Coding Tool": notes_texts,
        }

        allure_ref.attach(
            json.dumps(combined_data, indent=2),
            name="Notes Validation Data",
            attachment_type=allure_ref.attachment_type.JSON,
        )


@log_function_name
def test_document_deleted(
    driver,
    poc_submission_context,
    coding_tool_page,
):
    """
       Validate that the task created during POC submission
       can be successfully deleted using the Risk Coding Tool.

       This test_risk_poc ensures that:
       - The task link generated after submission is accessible
       - The delete action completes successfully
       - A successful deletion response is returned
       - User notification is triggered only after success
       """
    delete_result = coding_tool_page.delete_task(testdata_ref.delete_reason)

    allure_ref.attach(
        json.dumps(delete_result, indent=2),
        name="Delete Result",
        attachment_type=allure_ref.attachment_type.JSON,
    )

    assert delete_result.get("deleted"), delete_result.get("error")

    # ✅ Notify ONLY after successful assertions
    notify_success(
        title="POC Automation",
        message="Document deleted successfully ✅"
    )



@log_function_name
def test_deleted_document_not_in_documents(
    patient,
    poc_submission_context
):
    """
        Validate that a document deleted via the Risk Coding Tool
        is no longer visible in the Patient Dashboard document list.

        This test_risk_poc ensures that:
        - The patient document list can be retrieved successfully
        - The document deleted earlier does not appear in the list
        - UI state reflects backend deletion accurately
        """
    # Get deleted document name from submission context
    document_name = poc_submission_context.get("document_name")

    assert document_name, "Document name missing from submission context"

    # ---------------- STEP 1: Fetch documents from dashboard ----------------
    with allure_ref.step("Fetch document list from Patient Dashboard"):
        documents = patient.get_document_list()

        allure_ref.attach(
            json.dumps(documents, indent=2),
            name="Patient Documents List",
            attachment_type=allure_ref.attachment_type.JSON,
        )

        assert documents is not None, "Failed to fetch document list"

    # ---------------- STEP 2: Verify deleted document is NOT present ----------------
    with allure_ref.step("Verify deleted document is not present in documents list"):
        if document_name in documents:
            allure_ref.attach(
                document_name,
                name="Unexpected Document Found",
                attachment_type=allure_ref.attachment_type.TEXT,
            )

        assert document_name not in documents, (
            f"Deleted document '{document_name}' is still present in documents list"
        )