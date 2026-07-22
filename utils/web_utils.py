import time

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException, \
    StaleElementReferenceException, TimeoutException, NoSuchElementException


def debug_locator(driver, locator, friendly_name):
    print(f"--- Debugging {friendly_name} {locator} ---")
    els = driver.find_elements(*locator)
    print("LOCATOR TYPE:", type(locator))
    print("LOCATOR VALUE:", locator)
    print("matches count:", len(els))
    for i, el in enumerate(els):
        try:
            print(i, "displayed:", el.is_displayed())
            print(i, "outerHTML snippet:", el.get_attribute("outerHTML")[:600])
            print(i, "computed style:", driver.execute_script(
                "const e=arguments[0]; const s=window.getComputedStyle(e); return {display:s.display,visibility:s.visibility,opacity:s.opacity,rect:e.getBoundingClientRect()};",
                el))
        except Exception as e:
            print("error reading element", e)
    # check if inside iframe
    if len(els) == 0:
        print("No matches — checking frames...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print("iframe count:", len(iframes))
        for idx, f in enumerate(iframes):
            driver.switch_to.frame(f)
            matches = driver.find_elements(*locator)
            print(f"iframe[{idx}] matches:", len(matches))
            driver.switch_to.default_content()

from selenium.webdriver.common.keys import Keys
def move_cursor_space_and_backspace(element):
    element.send_keys(Keys.SPACE)
    time.sleep(0.3)
    element.send_keys(Keys.BACKSPACE)


def wait_for_inner_form_elements(driver,timeout=10):
    """
        Returns a WebDriverWait that retries every 0.2s for up to 2s(lets say timeout time = 2)
        while ignoring common element-not-ready exceptions.
        (~10 attempts max)
        """
    errors = [NoSuchElementException, ElementNotInteractableException]
    wait = WebDriverWait(driver, timeout, poll_frequency=.2, ignored_exceptions=errors)
    return wait


def sendkeys(driver,element,value):
    driver.execute_script(
        "arguments[0].value = arguments[1];"
        "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));"
        "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
        element,
        value
    )

def wait_or_scroll_to_element(driver, xpath, timeout=5):
    print(f"⏳ Waiting for element {xpath} to be visible...")

    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        print(f"✅{xpath} became visible without scrolling")
        return element

    except TimeoutException:
        print("🔄 Not visible yet, scrolling to element...")

        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of(element)
        )
        print(f"✅ {xpath} visible after scrolling")
        return element

def hover_on_element(driver, element):
    ActionChains(driver).move_to_element(element).perform()

def action_click(driver,element):
    try:
        element.click()
    except (ElementNotInteractableException, ElementClickInterceptedException,StaleElementReferenceException):

        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script("arguments[0].click();", element)

def wait_for_page_load(driver,timeout=30):
    loader_element_class = 'ajax_preloader'
    try:
        toast_msg = get_toast_message(driver)
        if toast_msg:
            print(toast_msg)
            allure.attach(
                toast_msg,
                name="Toast Message",
                attachment_type=allure.attachment_type.TEXT
            )
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, loader_element_class)))
    except TimeoutException as e:
        print(f"Ajax Preloader wait failed: {e} ")


def get_toast_message(driver, timeout=5):
    """
    Returns toast message text if visible, else None
    """
    try:
        toast = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@class,'toast') or contains(@class,'Toast')]")
            )
        )
        return toast.text.strip()
    except TimeoutException:
        return None