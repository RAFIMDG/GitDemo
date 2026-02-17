from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.config import Config


class WaitUtils:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EC_WAIT_TIME)

    def wait_for_visibility(self, locator):
        """Wait until element is visible"""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not visible: {locator}")

    def wait_for_clickable(self, locator):
        """Wait until element is clickable"""
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not clickable: {locator}")

    def wait_for_presence(self, locator):
        """Wait until element is present in DOM"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not present: {locator}")

    def wait_for_invisibility(self, locator):
        """Wait until element disappears"""
        try:
            return self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element still visible: {locator}")

    def wait_for_text(self, locator, text):
        """Wait until specific text appears in element"""
        try:
            return self.wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            raise TimeoutException(
                f"Text '{text}' not found in element: {locator}"
            )
