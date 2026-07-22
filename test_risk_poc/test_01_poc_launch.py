"""
Test Suite: POC Page – Core UI & Risk Validation

This test_risk_poc file validates the core behavior of the Risk POC page, including:
- Successful launch and rendering of the POC page
- Correct display of non-compliant DX codes
- Visibility and accuracy of Risk labels and counts
- Presence of essential UI elements required for user interaction

These tests ensure that the POC page is functionally usable and visually complete
from an end-user perspective.

Scope:
- UI validation
- Page-level business logic
- Non-destructive read-only checks
"""
import pytest
from utils.decorators import log_function_name
@log_function_name
def test_poc_launch(poc_page, patient_dashboard_data):
    """
    Validate that the Risk POC page launches successfully and
    displays the correct list of non-compliant DX codes
    as shown on the Patient Dashboard.
    """
    print("Testing POC Launch")

    dx_list = patient_dashboard_data["dx_list"]

    print("Expected DX list:", dx_list)

    poc_list = poc_page.get_visible_poc_dx_texts()

    print("POC DX list:", poc_list)

    assert poc_list == dx_list, (
        f"POC DX list mismatch.\nExpected: {dx_list}\nActual: {poc_list}"
    )

@log_function_name
def test_risk_label_and_count(poc_page, patient_dashboard_data):
    """
    Validate that the Risk label is displayed on the POC page and
    that the Risk count matches Patient Dashboard.
    """
    print("Testing Risk label and count")

    expected_count = patient_dashboard_data["risk_gaps"]

    visible = poc_page.is_risk_label_visible()
    print("Risk label visible:", visible)

    assert visible, "Risk Label is not displayed"

    label_text = poc_page.get_risk_label_text()
    count = poc_page.get_risk_count()

    print("Risk label text:", label_text)
    print("Risk count actual:", count)
    print("Risk count expected:", expected_count)

    assert "Risk" in label_text.strip(), "Risk label text incorrect"
    assert count == expected_count, (
        f"Risk count mismatch: expected {expected_count}, got {count}"
    )

@log_function_name
def test_poc_page_ui_elements(poc_page):
    """
    Validate that all core UI elements on the Risk POC page
    are present and visible.
    """
    print("Testing POC core UI elements")

    result = poc_page.visible_core_elements()

    for name, status in result.items():
        print(f"{name}: {'VISIBLE' if status else 'MISSING'}")

    missing = [name for name, status in result.items() if not status]

    assert not missing, f"Missing or hidden UI elements: {missing}"


@pytest.mark.xfail
@log_function_name
def test_poc_hierarchies_visibility(poc_page):
    """
    Verifies that HCC hierarchies are visible on the POC page.
    """
    print("Testing HCC hierarchy visibility")

    hierarchy_list = poc_page.get_hcc_hierarchies()
    print("Hierarchies found:", hierarchy_list)

    assert hierarchy_list, "No HCC hierarchies are displayed"


def test_invalid_poc_submission_missing_dos_or_provider(
    poc_invalid_submission_context
):
    """
    Validate that submitting POC without required fields
    shows validation toast.
    """
    print("Testing invalid POC submission")

    notif = poc_invalid_submission_context.get("notification")
    print("Validation toast:", notif)

    assert notif is not None, (
        "Expected validation toast, but none appeared"
    )

    assert any(
        phrase in notif.lower()
        for phrase in [
            "dos",
            "rendering provider",
            "should not be empty",
        ]
    ), f"Unexpected toast message: {notif}"