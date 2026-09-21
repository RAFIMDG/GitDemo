"""
Firefox Browser Driver
======================
Creates a Firefox WebDriver instance with configurable options.
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from drivers.browser import Browser
from utils.exceptions import DriverInitializationError
from utils.logger import get_logger

logger = get_logger(__name__)


class FirefoxBrowser(Browser):
    """Firefox WebDriver factory."""

    def create_driver(self) -> webdriver.Firefox | webdriver.Remote:
        """Create and return a configured Firefox driver."""
        options = self._build_options()

        try:
            grid_url = self.config.selenium_grid_url
            if grid_url:
                logger.info("Connecting to Selenium Grid at %s", grid_url)
                driver = webdriver.Remote(
                    command_executor=grid_url,
                    options=options,
                )
            else:
                logger.info("Starting local Firefox driver")
                service = Service(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)

            return self._apply_common_settings(driver)

        except Exception as e:
            raise DriverInitializationError("firefox", str(e))

    def _build_options(self) -> Options:
        """Build Firefox options from config."""
        options = Options()

        if self.config.headless:
            options.add_argument("--headless")
            logger.info("Firefox running in headless mode")

        # Performance / stability
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        options.set_preference("dom.webnotifications.enabled", False)

        return options
