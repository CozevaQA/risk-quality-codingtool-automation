import json
import re

import pytest

from pages.PatientDashboard import Patient_Dashboard
from utils.notifications import notify_success
from pages.RiskCodingTool import RiskCodingTool
from testresource import environment
from conftest import allure_ref, utility_ref, web_utility_ref, testdata_ref, pd_ref
from utils.decorators import log_function_name


@log_function_name
def test_confirmed_hcc_processed_to_stale(
    driver,
    patient,
    poc_submission_context
):
    """
        Validate that all confirmed HCC codes from POC submission
        are correctly reflected as stale HCC on the Patient Dashboard.


        """
    print("Checking confirmed HCCs")
    confirmed_hccs = poc_submission_context["confirmed_hccs"]
    with allure_ref.step("Collect stale HCC from patient dashboard"):
        processed_hcc_dx = patient.get_stale_hccs()

        allure_ref.attach(
            str(processed_hcc_dx),
            name="Processed HCCs",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        assert processed_hcc_dx, "No stale DX–HCC mappings found on patient dashboard"

    with allure_ref.step("Validate if confirmed hccs are in stale"):
        # ✅ Assert all confirmed HCCs exist in processed HCC list
        missing_hccs = set(confirmed_hccs) - set(processed_hcc_dx)

        assert not missing_hccs, (
            f"These confirmed HCCs are missing from dashboard: {missing_hccs}"
        )

        combined_data = {
            "Processed HCCs": processed_hcc_dx,
            "Confirmed hccs from POC": confirmed_hccs,
        }

        allure_ref.attach(
            json.dumps(combined_data, indent=2),
            name="Dashboard Data",
            attachment_type=allure_ref.attachment_type.JSON,
        )

@log_function_name
def test_confirmed_hcc_processed_to_hollow(
    driver,
    patient,
    poc_submission_context
):
    """
        Validate that all confirmed HCC codes from POC submission
        are correctly reflected with hollow dot HCC on the Patient Dashboard.


        """
    print("Checking confirmed HCCs")
    confirmed_hccs = poc_submission_context["confirmed_hccs"]
    with allure_ref.step("Collect stale HCC from patient dashboard"):
        hollow_hccs = patient.get_hollow_dot_hccs()

        allure_ref.attach(
            str(hollow_hccs),
            name="Hollow  HCCs",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        assert hollow_hccs, "No hollow HCC  found on patient dashboard"

    with allure_ref.step("Validate if confirmed hccs are in stale"):
        # ✅ Assert all confirmed HCCs exist in processed HCC list
        missing_hccs = set(confirmed_hccs) - set(hollow_hccs)

        assert not missing_hccs, (
            f"These confirmed HCCs are missing from dashboard: {missing_hccs}"
        )

        combined_data = {
            "Processed HCCs": hollow_hccs,
            "Confirmed hccs from POC": confirmed_hccs,
        }

        allure_ref.attach(
            json.dumps(combined_data, indent=2),
            name="Dashboard Data",
            attachment_type=allure_ref.attachment_type.JSON,
        )




@log_function_name
# @pytest.mark.parametrize("run_id", range(3))
def test_disconfirmed_hcc_processed_to_stale(
    patient,
    poc_submission_context,driver
):
    """
        Validate that all disconfirmed HCC codes from POC submission
        are correctly reflected as stale HCC on the Patient Dashboard.


        """
    print("Checking confirmed HCCs")
    disconfirmed_hccs = poc_submission_context["disconfirmed_hccs"]
    with allure_ref.step("Collect stale HCC from patient dashboard"):
        processed_hcc_dx = patient.get_stale_hccs()

        allure_ref.attach(
            str(processed_hcc_dx),
            name="Processed HCCs",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        assert processed_hcc_dx, "No stale DX–HCC mappings found on patient dashboard"

    with allure_ref.step("Validate if confirmed hccs are in stale"):
        # ✅ Assert all confirmed HCCs exist in processed HCC list
        missing_hccs = set(disconfirmed_hccs) - set(processed_hcc_dx)

        assert not missing_hccs, (
            f"These confirmed HCCs are missing from dashboard: {missing_hccs}"
        )

        combined_data = {
            "Processed HCCs": processed_hcc_dx,
            "Confirmed hccs from POC": disconfirmed_hccs,
        }

        allure_ref.attach(
            json.dumps(combined_data, indent=2),
            name="Dashboard Data",
            attachment_type=allure_ref.attachment_type.JSON,
        )


@log_function_name
def test_disconfirmed_hcc_processed_to_no_dot(
    driver,
    patient,
    poc_submission_context
):
    """
        Validate that all confirmed HCC codes from POC submission
        are correctly reflected with hollow dot HCC on the Patient Dashboard.


        """
    print("Checking Disconfirmed HCCs")
    disconfirmed_hccs = poc_submission_context["disconfirmed_hccs"]
    with allure_ref.step("Collect stale HCC from patient dashboard"):
        no_dot_hccs = patient.get_no_dot_hccs()

        allure_ref.attach(
            str(no_dot_hccs),
            name="Hollow  HCCs",
            attachment_type=allure_ref.attachment_type.TEXT,
        )

        assert no_dot_hccs, "No hollow HCC  found on patient dashboard"

    with allure_ref.step("Validate if confirmed hccs are in stale"):
        # ✅ Assert all confirmed HCCs exist in processed HCC list
        missing_hccs = set(disconfirmed_hccs) - set(no_dot_hccs)

        assert not missing_hccs, (
            f"These confirmed HCCs are missing from dashboard: {missing_hccs}"
        )

        combined_data = {
            "Processed HCCs": no_dot_hccs,
            "Confirmed hccs from POC": disconfirmed_hccs,
        }

        allure_ref.attach(
            json.dumps(combined_data, indent=2),
            name="Dashboard Data",
            attachment_type=allure_ref.attachment_type.JSON,
        )

