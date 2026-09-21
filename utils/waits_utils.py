"""
Wait Utilities
==============
Fluent, explicit-wait wrappers around Selenium's WebDriverWait.
Provides reusable wait methods with configurable timeouts and
automatic logging of wait outcomes.

Usage:
    from utils.waits_utils import WaitUtils

    wait = WaitUtils(driver)
    element = wait.wait_for_visibility((By.ID, "login-button"))
    wait.wait_for_url_contains("/inventory")
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config_manager import ConfigManager
from utils.exceptions import (
    ElementNotClickableError,
    ElementNotFoundError,
    ElementNotVisibleError,
    PageLoadTimeoutError,
)
from utils.logger import get_logger

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

logger = get_logger(__name__)


class WaitUtils:
    """Centralised explicit-wait helper bound to a driver instance."""

    IGNORED_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)

    def __init__(self, driver: "WebDriver", timeout: int | None = None) -> None:
        config = ConfigManager()
        self.driver = driver
        self.timeout = timeout or config.explicit_wait
        self.poll_frequency = float(config.get("timeouts.polling_interval", 0.5))

    # ── Private Helper ────────────────────────────────────────
    def _wait(self, timeout: int | None = None) -> WebDriverWait:
        """Return a configured ``WebDriverWait`` instance."""
        return WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=self.poll_frequency,
            ignored_exceptions=self.IGNORED_EXCEPTIONS,
        )

    # ── Element Waits ─────────────────────────────────────────
    def wait_for_visibility(
        self, locator: tuple, timeout: int | None = None
    ) -> "WebElement":
        """Wait until an element is visible in the viewport."""
        logger.debug("Waiting for visibility of %s (timeout=%ss)", locator, timeout or self.timeout)
        try:
            element = self._wait(timeout).until(EC.visibility_of_element_located(locator))
            logger.debug("Element visible: %s", locator)
            return element
        except TimeoutException:
            raise ElementNotVisibleError(str(locator), locator)

    def wait_for_clickable(
        self, locator: tuple, timeout: int | None = None
    ) -> "WebElement":
        """Wait until an element is clickable."""
        logger.debug("Waiting for clickability of %s", locator)
        try:
            element = self._wait(timeout).until(EC.element_to_be_clickable(locator))
            logger.debug("Element clickable: %s", locator)
            return element
        except TimeoutException:
            raise ElementNotClickableError(str(locator), locator)

    def wait_for_presence(
        self, locator: tuple, timeout: int | None = None
    ) -> "WebElement":
        """Wait until an element is present in the DOM (not necessarily visible)."""
        logger.debug("Waiting for presence of %s", locator)
        try:
            element = self._wait(timeout).until(EC.presence_of_element_located(locator))
            logger.debug("Element present: %s", locator)
            return element
        except TimeoutException:
            raise ElementNotFoundError(str(locator), locator)

    def wait_for_all_visible(
        self, locator: tuple, timeout: int | None = None
    ) -> list["WebElement"]:
        """Wait until *all* matching elements are visible."""
        logger.debug("Waiting for all elements visible: %s", locator)
        try:
            elements = self._wait(timeout).until(
                EC.visibility_of_all_elements_located(locator)
            )
            logger.debug("Found %d visible elements for %s", len(elements), locator)
            return elements
        except TimeoutException:
            raise ElementNotVisibleError(str(locator), locator)

    def wait_for_invisibility(
        self, locator: tuple, timeout: int | None = None
    ) -> bool:
        """Wait until an element is no longer visible."""
        logger.debug("Waiting for invisibility of %s", locator)
        try:
            return self._wait(timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            logger.warning("Element still visible after timeout: %s", locator)
            return False

    def wait_for_staleness(
        self, element: "WebElement", timeout: int | None = None
    ) -> bool:
        """Wait until an element is removed from the DOM (stale)."""
        logger.debug("Waiting for staleness of element")
        try:
            return self._wait(timeout).until(EC.staleness_of(element))
        except TimeoutException:
            return False

    # ── Text / Attribute Waits ────────────────────────────────
    def wait_for_text_present(
        self, locator: tuple, text: str, timeout: int | None = None
    ) -> bool:
        """Wait until the element's text contains ``text``."""
        logger.debug("Waiting for text '%s' in %s", text, locator)
        try:
            return self._wait(timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
        except TimeoutException:
            logger.warning("Text '%s' not found in %s", text, locator)
            return False

    def wait_for_attribute(
        self,
        locator: tuple,
        attribute: str,
        value: str,
        timeout: int | None = None,
    ) -> bool:
        """Wait until an element's attribute matches ``value``."""
        logger.debug("Waiting for %s[%s]='%s'", locator, attribute, value)

        def _attribute_matches(driver):
            el = driver.find_element(*locator)
            return el.get_attribute(attribute) == value

        try:
            return self._wait(timeout).until(_attribute_matches)
        except TimeoutException:
            return False

    # ── Navigation Waits ──────────────────────────────────────
    def wait_for_url_contains(
        self, url_fragment: str, timeout: int | None = None
    ) -> bool:
        """Wait until the current URL contains ``url_fragment``."""
        logger.debug("Waiting for URL to contain '%s'", url_fragment)
        try:
            return self._wait(timeout).until(EC.url_contains(url_fragment))
        except TimeoutException:
            raise PageLoadTimeoutError(url_fragment, timeout or self.timeout)

    def wait_for_url_to_be(
        self, url: str, timeout: int | None = None
    ) -> bool:
        """Wait until the current URL exactly equals ``url``."""
        logger.debug("Waiting for URL to be '%s'", url)
        try:
            return self._wait(timeout).until(EC.url_to_be(url))
        except TimeoutException:
            raise PageLoadTimeoutError(url, timeout or self.timeout)

    def wait_for_title_contains(
        self, title_fragment: str, timeout: int | None = None
    ) -> bool:
        """Wait until the page title contains ``title_fragment``."""
        logger.debug("Waiting for title to contain '%s'", title_fragment)
        try:
            return self._wait(timeout).until(EC.title_contains(title_fragment))
        except TimeoutException:
            return False

    # ── Frame / Window Waits ──────────────────────────────────
    def wait_for_frame(
        self, frame_locator, timeout: int | None = None
    ) -> "WebDriver":
        """Wait until a frame is available and switch to it."""
        logger.debug("Waiting for frame: %s", frame_locator)
        try:
            return self._wait(timeout).until(
                EC.frame_to_be_available_and_switch_to_it(frame_locator)
            )
        except TimeoutException:
            raise ElementNotFoundError(f"Frame: {frame_locator}")

    def wait_for_new_window(
        self, current_handles: list[str], timeout: int | None = None
    ) -> bool:
        """Wait until a new window/tab appears."""
        logger.debug("Waiting for new window (current: %d)", len(current_handles))
        try:
            return self._wait(timeout).until(EC.new_window_is_opened(current_handles))
        except TimeoutException:
            return False

    # ── Alert Waits ───────────────────────────────────────────
    def wait_for_alert(self, timeout: int | None = None):
        """Wait until a JavaScript alert is present and return it."""
        logger.debug("Waiting for alert")
        try:
            return self._wait(timeout).until(EC.alert_is_present())
        except TimeoutException:
            logger.warning("No alert appeared within timeout")
            return None

    # ── JavaScript Waits ──────────────────────────────────────
    def wait_for_page_load(self, timeout: int | None = None) -> bool:
        """Wait until ``document.readyState`` is ``complete``."""
        logger.debug("Waiting for page load (document.readyState)")
        try:
            return self._wait(timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach readyState=complete")
            return False

    def wait_for_ajax(self, timeout: int | None = None) -> bool:
        """Wait until jQuery AJAX requests are complete (if jQuery is present)."""
        logger.debug("Waiting for AJAX completion")
        try:
            return self._wait(timeout).until(
                lambda d: d.execute_script(
                    "return typeof jQuery !== 'undefined' ? jQuery.active === 0 : true"
                )
            )
        except TimeoutException:
            logger.warning("AJAX requests did not complete within timeout")
            return False
