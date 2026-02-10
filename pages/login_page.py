from selenium.webdriver.common.by import By
from Seleniumpractice.pages.base_page import BasePage
from Seleniumpractice.utils.config import Config


class LoginPage(BasePage):

    # ===== LOCATORS =====
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MSG = (By.XPATH, "//h3[@data-test='error']")

    # ===== ACTIONS =====
    def login(self, username, password):
        """Login with provided credentials"""
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def login_as_standard_user(self):
        """Login using default credentials from config"""
        self.login(Config.USERNAME, Config.PASSWORD)

    # ===== VALIDATIONS =====
    def get_error_message(self):
        """Return login error message text"""
        return self.get_text(self.ERROR_MSG)

    def is_login_error_displayed(self):
        """Check if login error is visible"""
        return self.wait.wait_for_visibility(self.ERROR_MSG)
