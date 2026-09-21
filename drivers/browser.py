"""
Browser Abstract Base Class
============================
Defines the contract every browser driver must implement.
Concrete subclasses (Chrome, Firefox, Edge) extend this to provide
browser-specific options and initialisation logic.

Usage:
    # Not used directly — see ChromeBrowser, FirefoxBrowser, EdgeBrowser.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from config.config_manager import ConfigManager
from utils.logger import get_logger

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

logger = get_logger(__name__)


class Browser(ABC):
    """Abstract base for browser driver factories."""

    def __init__(self) -> None:
        self.config = ConfigManager()

    @abstractmethod
    def create_driver(self) -> "WebDriver":
        """Create and return a configured WebDriver instance."""
        ...

    def _apply_common_settings(self, driver: "WebDriver") -> "WebDriver":
        """Apply timeouts and window settings shared across all browsers."""
        driver.implicitly_wait(self.config.implicit_wait)
        driver.set_page_load_timeout(self.config.page_load_timeout)
        driver.maximize_window()
        logger.info(
            "Driver configured — implicit_wait=%ds, page_load=%ds",
            self.config.implicit_wait,
            self.config.page_load_timeout,
        )
        return driver
