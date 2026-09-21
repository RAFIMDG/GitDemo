"""
Login Page Object
=================
Page object for the SauceDemo login page.
"""

from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from config.config_manager import ConfigManager
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("Authentication")
class LoginPage(BasePage):
    """SauceDemo Login Page."""

    # ===== LOCATORS =====
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MSG = (By.XPATH, "//h3[@data-test='error']")
    ERROR_BTN = (By.CLASS_NAME, "error-button")

    # ===== ACTIONS =====
    @allure.step("Login with username: {username}")
    def login(self, username: str, password: str) -> None:
        """Login with provided credentials."""
        logger.info("Logging in as: %s", username)
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    @allure.step("Login as standard user")
    def login_as_standard_user(self) -> None:
        """Login using default credentials from config."""
        config = ConfigManager()
        self.login(config.username, config.password)

    # ===== VALIDATIONS =====
    @allure.step("Get login error message")
    def get_error_message(self) -> str:
        """Return login error message text."""
        text = self.get_text(self.ERROR_MSG)
        logger.info("Error message: %s", text)
        return text

    @allure.step("Check if login error is displayed")
    def is_login_error_displayed(self) -> bool:
        """Check if login error is visible."""
        return self.is_element_displayed(self.ERROR_MSG)

    @allure.step("Clear login error")
    def clear_error(self) -> None:
        """Click the X button to dismiss the error."""
        if self.is_element_displayed(self.ERROR_BTN):
            self.click(self.ERROR_BTN)

    @allure.step("Verify login page is loaded")
    def is_login_page_loaded(self) -> bool:
        """Verify the login page elements are present."""
        return (
            self.is_element_displayed(self.USERNAME)
            and self.is_element_displayed(self.PASSWORD)
            and self.is_element_displayed(self.LOGIN_BTN)
        )
