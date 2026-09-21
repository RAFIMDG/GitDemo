"""
Base Page Object
================
Foundation class for all page objects. Provides common interaction
methods (click, type, get_text, select, scroll, etc.) backed by
explicit waits and structured logging.

Every page object should inherit from ``BasePage`` and call
``super().__init__(driver)`` in its constructor.

Usage:
    class LoginPage(BasePage):
        USERNAME = (By.ID, "user-name")

        def enter_username(self, text):
            self.type(self.USERNAME, text)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from utils.logger import get_logger
from utils.screenshots import ScreenshotManager
from utils.waits_utils import WaitUtils

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

logger = get_logger(__name__)


class BasePage:
    """
    Abstract base page. All page objects inherit from here.

    Attributes:
        driver:     Selenium WebDriver instance.
        wait:       WaitUtils helper bound to this driver.
        screenshot: ScreenshotManager for capturing evidence.
    """

    def __init__(self, driver: "WebDriver") -> None:
        self.driver = driver
        self.wait = WaitUtils(driver)
        self.screenshot = ScreenshotManager(driver)

    # ── Navigation ────────────────────────────────────────────
    @allure.step("Navigate to {url}")
    def navigate_to(self, url: str) -> None:
        """Open a URL in the browser."""
        logger.info("Navigating to: %s", url)
        self.driver.get(url)
        self.wait.wait_for_page_load()

    @allure.step("Navigate back")
    def go_back(self) -> None:
        """Press the browser Back button."""
        self.driver.back()
        self.wait.wait_for_page_load()

    @allure.step("Refresh page")
    def refresh(self) -> None:
        """Reload the current page."""
        self.driver.refresh()
        self.wait.wait_for_page_load()

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def page_title(self) -> str:
        return self.driver.title

    # ── Element Interactions ──────────────────────────────────
    @allure.step("Click element: {locator}")
    def click(self, locator: tuple) -> None:
        """Wait for element to be clickable, then click."""
        logger.debug("Clicking: %s", locator)
        self.wait.wait_for_clickable(locator).click()

    @allure.step("Type '{text}' into {locator}")
    def type(self, locator: tuple, text: str) -> None:
        """Clear a field and type text into it."""
        logger.debug("Typing '%s' into %s", text, locator)
        element = self.wait.wait_for_visibility(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Get text from {locator}")
    def get_text(self, locator: tuple) -> str:
        """Return the visible text of an element."""
        text = self.wait.wait_for_visibility(locator).text
        logger.debug("Got text '%s' from %s", text, locator)
        return text

    def get_attribute(self, locator: tuple, attribute: str) -> str | None:
        """Return the value of an element's attribute."""
        return self.wait.wait_for_visibility(locator).get_attribute(attribute)

    def is_element_displayed(self, locator: tuple, timeout: int = 3) -> bool:
        """Check if an element is displayed (short timeout to avoid blocking)."""
        try:
            self.wait.wait_for_visibility(locator, timeout=timeout)
            return True
        except Exception:
            return False

    def is_element_present(self, locator: tuple, timeout: int = 3) -> bool:
        """Check if an element is present in the DOM."""
        try:
            self.wait.wait_for_presence(locator, timeout=timeout)
            return True
        except Exception:
            return False

    # ── Multi-Element Operations ──────────────────────────────
    def get_elements(self, locator: tuple) -> list["WebElement"]:
        """Return all matching visible elements."""
        return self.wait.wait_for_all_visible(locator)

    def get_elements_text(self, locator: tuple) -> list[str]:
        """Return the text of all matching elements."""
        elements = self.get_elements(locator)
        return [el.text for el in elements]

    def get_element_count(self, locator: tuple) -> int:
        """Return the number of matching elements."""
        return len(self.driver.find_elements(*locator))

    # ── Dropdown / Select ─────────────────────────────────────
    @allure.step("Select '{value}' from {locator}")
    def select_by_value(self, locator: tuple, value: str) -> None:
        """Select a <select> option by its ``value`` attribute."""
        element = self.wait.wait_for_visibility(locator)
        Select(element).select_by_value(value)

    def select_by_visible_text(self, locator: tuple, text: str) -> None:
        """Select a <select> option by its visible text."""
        element = self.wait.wait_for_visibility(locator)
        Select(element).select_by_visible_text(text)

    def select_by_index(self, locator: tuple, index: int) -> None:
        """Select a <select> option by index."""
        element = self.wait.wait_for_visibility(locator)
        Select(element).select_by_index(index)

    def get_selected_option_text(self, locator: tuple) -> str:
        """Return the text of the currently selected option."""
        element = self.wait.wait_for_visibility(locator)
        return Select(element).first_selected_option.text

    # ── Mouse Actions ─────────────────────────────────────────
    @allure.step("Hover over {locator}")
    def hover(self, locator: tuple) -> None:
        """Move the mouse over an element."""
        element = self.wait.wait_for_visibility(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def double_click(self, locator: tuple) -> None:
        """Double-click an element."""
        element = self.wait.wait_for_clickable(locator)
        ActionChains(self.driver).double_click(element).perform()

    def right_click(self, locator: tuple) -> None:
        """Right-click (context menu) an element."""
        element = self.wait.wait_for_clickable(locator)
        ActionChains(self.driver).context_click(element).perform()

    def drag_and_drop(self, source_locator: tuple, target_locator: tuple) -> None:
        """Drag one element onto another."""
        source = self.wait.wait_for_visibility(source_locator)
        target = self.wait.wait_for_visibility(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    # ── Scrolling ─────────────────────────────────────────────
    def scroll_to_element(self, locator: tuple) -> None:
        """Scroll until an element is in view."""
        element = self.wait.wait_for_presence(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element,
        )

    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_top(self) -> None:
        """Scroll to the top of the page."""
        self.driver.execute_script("window.scrollTo(0, 0);")

    # ── JavaScript Helpers ────────────────────────────────────
    def js_click(self, locator: tuple) -> None:
        """Click via JavaScript (bypasses overlays/interception)."""
        element = self.wait.wait_for_presence(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def js_set_value(self, locator: tuple, value: str) -> None:
        """Set an input's value via JavaScript."""
        element = self.wait.wait_for_presence(locator)
        self.driver.execute_script(f"arguments[0].value = '{value}';", element)

    def execute_script(self, script: str, *args) -> any:
        """Execute arbitrary JavaScript."""
        return self.driver.execute_script(script, *args)

    # ── Frame / Window ────────────────────────────────────────
    def switch_to_frame(self, frame_locator: tuple) -> None:
        """Switch to an iframe."""
        self.wait.wait_for_frame(frame_locator)

    def switch_to_default_content(self) -> None:
        """Switch back to the main document from an iframe."""
        self.driver.switch_to.default_content()

    def switch_to_window(self, window_handle: str) -> None:
        """Switch to a specific browser window/tab."""
        self.driver.switch_to.window(window_handle)

    @property
    def window_handles(self) -> list[str]:
        return self.driver.window_handles
