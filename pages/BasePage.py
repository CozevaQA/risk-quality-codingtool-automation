
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.timeout = timeout

    def wait_for_element(self, by_locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(by_locator)
        )

    def wait_for_clickable(self, by_locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(by_locator)
        )

    def wait_for_all_elements_present(self, by_locator, timeout=5):
        """
        Wait until at least one element exists in DOM.
        (Not visibility, just presence)
        """
        wait_timeout = timeout if timeout else self.timeout
        return WebDriverWait(self.driver, wait_timeout).until(
            EC.presence_of_all_elements_located(by_locator)
        )

    def is_visible_and_displayed(self, locator, timeout=10):
        """
        Returns True only if:
        - element becomes visible within timeout
        - AND element.is_displayed() == True
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except:
            return False