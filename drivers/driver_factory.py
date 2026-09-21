"""
Driver Factory
==============
Central factory that creates the correct WebDriver based on
configuration or CLI parameter.

Usage:
    from drivers.driver_factory import DriverFactory

    driver = DriverFactory.create_driver("chrome")  # explicit
    driver = DriverFactory.create_driver()           # from config
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from config.config_manager import ConfigManager
from drivers.chrome import ChromeBrowser
from drivers.edge import EdgeBrowser
from drivers.firefox import FirefoxBrowser
from utils.exceptions import BrowserNotSupportedError
from utils.logger import get_logger

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

logger = get_logger(__name__)

# Registry of supported browsers
_BROWSER_REGISTRY: dict[str, type] = {
    "chrome": ChromeBrowser,
    "firefox": FirefoxBrowser,
    "edge": EdgeBrowser,
}


class DriverFactory:
    """Factory for creating WebDriver instances."""

    @staticmethod
    def create_driver(browser_name: str | None = None) -> "WebDriver":
        """
        Create and return a WebDriver instance.

        Args:
            browser_name: ``"chrome"`` | ``"firefox"`` | ``"edge"``.
                          Falls back to config if ``None``.

        Returns:
            A configured, maximised WebDriver.

        Raises:
            BrowserNotSupportedError: If the browser name is invalid.
        """
        config = ConfigManager()
        name = (browser_name or config.browser).lower().strip()

        browser_class = _BROWSER_REGISTRY.get(name)
        if not browser_class:
            raise BrowserNotSupportedError(name)

        logger.info("Creating %s driver", name.capitalize())
        return browser_class().create_driver()
