from utils.waits_utils import WaitUtils


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WaitUtils(driver)

    def click(self, locator):
        self.wait.wait_for_clickable(locator).click()

    def type(self, locator, text):
        element = self.wait.wait_for_visibility(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.wait.wait_for_visibility(locator).text

    def is_visible(self, locator):
        return self.wait.wait_for_visibility(locator)
