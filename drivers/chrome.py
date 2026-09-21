"""
Chrome Browser Driver
=====================
Creates a Chrome WebDriver instance with configurable options
including headless mode, Selenium Grid support, and common
stability flags.
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from drivers.browser import Browser
from utils.exceptions import DriverInitializationError
from utils.logger import get_logger

logger = get_logger(__name__)


class ChromeBrowser(Browser):
    """Chrome WebDriver factory."""

    def create_driver(self) -> webdriver.Chrome | webdriver.Remote:
        """Create and return a configured Chrome driver."""
        options = self._build_options()

        try:
            # Use Selenium Grid if configured
            grid_url = self.config.selenium_grid_url
            if grid_url:
                logger.info("Connecting to Selenium Grid at %s", grid_url)
                driver = webdriver.Remote(
                    command_executor=grid_url,
                    options=options,
                )
            else:
                logger.info("Starting local Chrome driver")
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)

            return self._apply_common_settings(driver)

        except Exception as e:
            raise DriverInitializationError("chrome", str(e))

    def _build_options(self) -> Options:
        """Build Chrome options from config."""
        options = Options()

        if self.config.headless:
            options.add_argument("--headless=new")
            logger.info("Chrome running in headless mode")

        # Stability flags
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")

        # Suppress logging noise
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            },
        )

        return options
