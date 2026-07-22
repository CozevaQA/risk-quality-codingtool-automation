"""
Test Suite: DX–HCC Population & Mapping Validation

This test_risk_poc file validates the correctness of DX to HCC population logic, ensuring:
- Diagnoses displayed in the application are correctly mapped to HCC categories
- HCC population is consistent across Commercial, Medicaid, and Risk workflows
- Source DX codes align with reference mapping files
- Last DOS and data integrity rules are correctly applied

These tests focus on data accuracy and backend-driven business rules rather than UI behavior.

Scope:
- Data validation
- Business rule enforcement
- Mapping accuracy against reference sources
"""
from conftest import allure_ref, utility_ref, web_utility_ref, testdata_ref, pd_ref
from utils.decorators import log_function_name
import pytest
@log_function_name
def test_dx_hcc_population(poc_page):
    """
    Validate that DX codes displayed on the Risk POC page are correctly
    populated with their corresponding HCC details and metadata.
    """

    print("TEST: DX → HCC population validation")

    dx_desc_last_dos = poc_page.get_dx_dos_rows()
    print("Total DX rows found:", len(dx_desc_last_dos))

    # Get mapping file based on HCC type
    hcc_file = utility_ref.get_mapping_file_path(testdata_ref.hcc_type)
    print("Using HCC mapping file:", hcc_file)

    df = pd_ref.read_csv(hcc_file)

    report_lines = []
    failures = []

    for hcc_id, hcc_desc, dx_description, dx_code, last_dos in dx_desc_last_dos:

        normalized_dx_code = dx_code.replace(".", "")
        row = df.loc[df["DXCode"] == normalized_dx_code]

        # --- DX code not found ---
        if row.empty:
            msg = (
                f"[FAIL] DX Code not found in mapping CSV\n"
                f"DX Code: {dx_code}\n"
                f"Last DOS: {last_dos}"
            )
            report_lines.append(msg)
            failures.append(msg)
            continue

        row = row.iloc[0]
        expected_description = str(row["Description"]).strip()

        # --- Validate DOS format ---
        is_dos_valid = utility_ref.is_valid_date(last_dos)

        # --- Description validation ---
        if expected_description == dx_description:
            report_lines.append(
                f"[PASS] {dx_code} → Description matched"
            )
        else:
            msg = (
                f"[FAIL] {dx_code} → Description mismatch\n"
                f"Expected: {expected_description}\n"
                f"Actual:   {dx_description}"
            )
            report_lines.append(msg)
            failures.append(msg)

        # ---------------- HCC ID ---------------- #
        if pd_ref.notna(row["V28ID"]):
            expected_hcc_id = str(int(row["V28ID"]))
        else:
            expected_hcc_id = ""

        if expected_hcc_id == str(hcc_id):
            report_lines.append(
                f"[PASS] {dx_code} → HCC ID matched ({hcc_id})"
            )
        else:
            msg = (
                f"[FAIL] {dx_code} → HCC ID mismatch\n"
                f"Expected: {expected_hcc_id}\n"
                f"Actual:   {hcc_id}"
            )
            report_lines.append(msg)
            failures.append(msg)

        # ---------------- HCC DESCRIPTION ---------------- #
        expected_hcc_desc = str(row["V28HCCDescription"])

        if expected_hcc_desc == hcc_desc:
            report_lines.append(
                f"[PASS] {dx_code} → HCC Description matched"
            )
        else:
            msg = (
                f"[FAIL] {dx_code} → HCC Description mismatch\n"
                f"Expected: {expected_hcc_desc}\n"
                f"Actual:   {hcc_desc}"
            )
            report_lines.append(msg)
            failures.append(msg)

        # --- DOS validation ---
        if is_dos_valid:
            report_lines.append(
                f"[PASS] {dx_code} → Last DOS format valid ({last_dos})"
            )
        else:
            msg = (
                f"[FAIL] {dx_code} → Invalid Last DOS format\n"
                f"Value: {last_dos}\n"
                f"Expected format: MM/DD/YYYY"
            )
            report_lines.append(msg)
            failures.append(msg)

    # 📎 Attach full validation report to Allure
    report_text = "\n\n".join(report_lines)
    allure_ref.attach(
        report_text,
        name="DX Description & DOS ICD10 Validation",
        attachment_type=allure_ref.attachment_type.TEXT
    )

    # Final assertion (single point of failure)
    assert not failures, (
        f"{len(failures)} validation(s) failed.\n\n"
        + "\n\n".join(failures)
    )