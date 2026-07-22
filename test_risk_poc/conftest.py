import os
import shutil
import time

import pytest
import pandas as pd
import allure

from pages.RiskCodingTool import RiskCodingTool
from utils import common_utils as utility
from utils import common_utils, web_utils
from utils import web_utils as webfunctions

from testresource import testdata, environment
from testresource.environment import (
    username,
    password,
    submit,
    reason_textbox, CHROME_PROFILE, LOGIN_URL, USERNAME, PASSWORD, REASON
)

from pages.PatientDashboard import Patient_Dashboard
from pages.RiskPOC import Risk_POC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.chrome.service import Service as ChromeService, Service
from selenium.webdriver.edge.service import Service as EdgeService


from selenium.webdriver.common.by import By

from utils.notifications import notify_success

allure_ref = allure
utility_ref = utility
web_utility_ref = webfunctions
testdata_ref = testdata
pd_ref = pd


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "edge"],
        help="Browser to run test_risk_poc on",
    )

# Clean up old allure-results for fresh execution
@pytest.fixture(scope="session", autouse=True)
def clean_allure_results():
    results_dir = "allure-results"

    # delete existing directory if present
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
        print(f"[Allure] Cleaned old results at: {results_dir}")

    # recreate empty folder
    os.makedirs(results_dir, exist_ok=True)

    yield   # nothing needed after the session

@pytest.fixture(scope="session")
def driver(request):
    browser = request.config.getoption("--browser")
    # 👉 Check if profile folder exists, else create it
    if not os.path.exists(CHROME_PROFILE):
        os.makedirs(CHROME_PROFILE)
        print(f"Created Chrome profile directory: {CHROME_PROFILE}")
    else:
        print(f"Using existing Chrome profile directory: {CHROME_PROFILE}")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        service = Service(executable_path="testresource/chromedriver.exe")
        # 👉 Chrome profile setup
        options.add_argument(f"--user-data-dir={CHROME_PROFILE}")
        options.add_argument("--profile-directory=Default")     # or Profile 1
        options.add_experimental_option("detach", True)
        drv = webdriver.Chrome(
            service=service,
            options=options,
        )

    elif browser == "edge":
        options = webdriver.EdgeOptions()

        # 👉 Edge profile setup
        edge_profile_path = os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data")
        options.add_argument(f"--user-data-dir={edge_profile_path}")
        options.add_argument("--profile-directory=Default")     # or Profile 1
        options.add_experimental_option("detach", True)
        # drv = webdriver.Edge(
        #     service=EdgeService(EdgeChromiumDriverManager().install()),
        #     options=options,
        # )
    # drv.implicitly_wait(2)
    drv.maximize_window()
    yield drv
    drv.quit()

#
@pytest.fixture(scope="session", autouse=True)
def login_once(driver):
    """
    Runs ONCE before any test_risk_poc (session scoped) and logs in.
    All test_risk_poc will see an already logged-in browser.
    """
    # Go to login page
    driver.get(LOGIN_URL)
    driver.maximize_window()

    wait= WebDriverWait(driver, 120)
    #  Enter username
    uname_el = wait.until(EC.presence_of_element_located((By.ID, username)))
    uname_el.clear()
    uname_el.send_keys(common_utils.decode_base64(USERNAME))

    #  Enter password
    pwd_el = driver.find_element(By.ID, password)
    pwd_el.clear()
    pwd_el.send_keys(common_utils.decode_base64(PASSWORD))

    #  Submit login (first submit)
    submit_el = wait.until(EC.element_to_be_clickable((By.ID, submit)))
    submit_el.click()

    # --------------- ALWAYS ENTER REASON ---------------- #

    #  Wait for reason textbox
    reason_el = wait.until(
        EC.presence_of_element_located((By.XPATH, reason_textbox))
    )

    #  Enter reason
    actions = ActionChains(driver)
    actions.move_to_element(reason_el).click().send_keys(REASON).perform()

    # Submit again (second submit)
    submit_el2 = wait.until(EC.element_to_be_clickable((By.ID, submit)))
    submit_el2.click()
    webfunctions.wait_for_page_load(driver, 120)

@pytest.fixture(scope="session")
def patient_dashboard_data(driver):
    try:
        with allure.step("Open Patient Dashboard"):
            print("Opening Patient Dashboard for:", testdata.patient_cozeva_id)
            patient = Patient_Dashboard(driver, 30, testdata.patient_cozeva_id)
            assert patient.open_patient_dashboard(environment.BASE_URL), \
                "Failed to open patient dashboard."

        with allure.step("Fetch Non-Compliant DX from Patient Dashboard"):
            dx_list = patient.get_non_compliant_dx()
            dx_count = len(dx_list)

            print("DX count from dashboard:", dx_count)

            allure.attach(
                str(dx_list),
                "Non-Compliant DX List",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                str(dx_count),
                "Non-Compliant DX Count",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Fetch Risk Gaps from Patient Dashboard"):
            risk_gaps = patient.get_risk_gaps()
            print("Risk gaps:", risk_gaps)

            allure.attach(
                str(risk_gaps),
                "Risk Gaps",
                attachment_type=allure.attachment_type.TEXT
            )

        return {
            "patient": patient,
            "dx_list": dx_list,
            "dx_count": dx_count,
            "risk_gaps": risk_gaps,
            "hcc_gaps_list": None,
            "total_hcc_list": None
        }

    except Exception as e:
        print("ERROR in patient_dashboard_data fixture:", str(e))
        allure.attach(
            str(e),
            "patient_dashboard_data ERROR",
            attachment_type=allure.attachment_type.TEXT
        )
        raise

@pytest.fixture(scope="session")
def poc_page(driver, patient_dashboard_data):
    try:
        with allure.step("Open Risk POC Page"):
            print("Opening POC page")
            patient = patient_dashboard_data["patient"]
            risk_poc = patient.open_poc()
            assert risk_poc.is_page_loaded(), "POC page did not load properly"

        with allure.step("Expand Show DX on POC Page"):
            visible_show_dx_clicked = risk_poc.click_visible_show_dx_buttons()
            print("Show DX clicked:", visible_show_dx_clicked)

            allure.attach(
                str(visible_show_dx_clicked),
                "Show DX Buttons Clicked",
                attachment_type=allure.attachment_type.TEXT
            )

        return risk_poc

    except Exception as e:
        print("ERROR in poc_page fixture:", str(e))
        allure.attach(
            str(e),
            "poc_page ERROR",
            attachment_type=allure.attachment_type.TEXT
        )
        raise


@pytest.fixture(scope="module")
def recapture_context(poc_page):
    """
    Executes recapture action once and
    stores the acted DX context.
    """
    try:
        context = poc_page.recapture_confirm()
        print("Recapture context:", context)
        return context
    except Exception as e:
        print("ERROR in recapture_context:", str(e))
        raise


@pytest.fixture(scope="module")
def disconfirm_context(poc_page):
    """
    Executes disconfirm action once on the first
    eligible Recapture DX and returns the observed context.
    """
    try:
        context = poc_page.recapture_disconfirm()
        print("Disconfirm context:", context)
        return context
    except Exception as e:
        print("ERROR in disconfirm_context:", str(e))
        raise

@pytest.fixture(scope="module")
def not_addressed_context(poc_page):
    """
        Executes not addressed action once on the first
        eligible Recapture DX and returns the observed context.
        """

    try:
        context = poc_page.mark_as_not_addressed()
        print("Not Addressed context:", context)
        return context
    except Exception as e:
        print("ERROR in not_addressed_context:", str(e))
        raise


@pytest.fixture(scope="module")
def patient(driver):
    """
    Provides Patient_Dashboard object scoped only to test_patient_dashboard module.
    """
    patient = Patient_Dashboard(
        driver,
        30,
        testdata_ref.patient_cozeva_id
    )

    patient.open_patient_dashboard(environment.BASE_URL)
    web_utility_ref.wait_for_page_load(driver, 120)
    return patient


@pytest.fixture(scope="module")
def coding_tool_page(driver,poc_submission_context):
    """ Provides page object of coding tool of a task link """
    task_link = poc_submission_context["task_link"]
    assert task_link, "Task link missing"

    driver.get(task_link)

    with allure_ref.step("Verify Risk Coding Tool page is loaded"):
        web_utility_ref.wait_for_page_load(driver, 120)

    with allure_ref.step("Delete Task"):
        risk_coding_tool = RiskCodingTool(driver)

    return risk_coding_tool

### Send notifications of not run modules


executed_modules = set()
collected_modules = set()


def pytest_collection_modifyitems(session, config, items):
    # Collect all modules that pytest found
    for item in items:
        collected_modules.add(item.module.__file__)


def pytest_runtest_logreport(report):
    # Track modules that actually executed
    if report.when == "call" and report.passed or report.failed:
        executed_modules.add(report.nodeid.split("::")[0])


def pytest_sessionfinish(session, exitstatus):

    not_executed = collected_modules - executed_modules

    if not_executed:
        print("\n⚠️ These test files were collected but not executed:")
        for module in not_executed:
            print(module)
        count = len(not_executed)

        notify_success(
            title="Missing Test Files",
            message=f"{count} test files were not executed. Check logs.",
        )




@pytest.fixture(scope="session")
def poc_submission_context(poc_page):
    """
    Executes POC submission and stores result.
    """
    try:
        result = poc_page.SubmitPOC(invalid_submission=False)
        print("POC submission result:", result)

        if result.get("error"):
            pytest.fail(f"POC submission failed: {result['error']}")

        return result
    except Exception as e:
        print("ERROR in poc_submission_context:", str(e))
        raise

@pytest.fixture(scope="session")
def poc_invalid_submission_context(poc_page):
    """
    Executes INVALID POC submission and stores result.
    """
    try:
        result = poc_page.SubmitPOC(invalid_submission=True)
        print("Invalid POC submission result:", result)
        return result
    except Exception as e:
        print("ERROR in poc_invalid_submission_context:", str(e))
        raise

@pytest.fixture(autouse=True)
def slow_down_between_tests():
    time.sleep(2)   # before test_risk_poc
    yield
    time.sleep(2)   # after test_risk_poc