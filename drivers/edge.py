"""
Edge Browser Driver
===================
Creates a Microsoft Edge WebDriver instance with configurable options.
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from drivers.browser import Browser
from utils.exceptions import DriverInitializationError
from utils.logger import get_logger

logger = get_logger(__name__)


class EdgeBrowser(Browser):
    """Edge (Chromium) WebDriver factory."""

    def create_driver(self) -> webdriver.Edge | webdriver.Remote:
        """Create and return a configured Edge driver."""
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
                logger.info("Starting local Edge driver")
                service = Service(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=options)

            return self._apply_common_settings(driver)

        except Exception as e:
            raise DriverInitializationError("edge", str(e))

    def _build_options(self) -> Options:
        """Build Edge options from config."""
        options = Options()

        if self.config.headless:
            options.add_argument("--headless=new")
            logger.info("Edge running in headless mode")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        return options
