"""
Custom Framework Exceptions
============================
Domain-specific exceptions for the SauceDemo automation framework.
Provides granular error classification for better debugging, reporting,
and retry logic.

Usage:
    from utils.exceptions import ElementNotFoundError, PageLoadTimeoutError

    raise ElementNotFoundError("Login button", (By.ID, "login-button"))
"""

from __future__ import annotations

from typing import Any


class FrameworkError(Exception):
    """Base exception for all framework errors."""

    def __init__(self, message: str = "", details: Any = None) -> None:
        self.details = details
        super().__init__(message)


# ──────────────────────────────────────────────────────────────
# Element Interaction Errors
# ──────────────────────────────────────────────────────────────

class ElementNotFoundError(FrameworkError):
    """Raised when an element cannot be located in the DOM."""

    def __init__(self, element_name: str, locator: tuple | None = None) -> None:
        self.element_name = element_name
        self.locator = locator
        msg = f"Element '{element_name}' not found"
        if locator:
            msg += f" using locator {locator}"
        super().__init__(msg, details={"element": element_name, "locator": locator})


class ElementNotClickableError(FrameworkError):
    """Raised when an element is present but not clickable."""

    def __init__(self, element_name: str, locator: tuple | None = None) -> None:
        self.element_name = element_name
        self.locator = locator
        msg = f"Element '{element_name}' is not clickable"
        if locator:
            msg += f" using locator {locator}"
        super().__init__(msg, details={"element": element_name, "locator": locator})


class ElementNotVisibleError(FrameworkError):
    """Raised when an element exists in DOM but is not visible."""

    def __init__(self, element_name: str, locator: tuple | None = None) -> None:
        msg = f"Element '{element_name}' is present but not visible"
        if locator:
            msg += f" using locator {locator}"
        super().__init__(msg, details={"element": element_name, "locator": locator})


# ──────────────────────────────────────────────────────────────
# Page / Navigation Errors
# ──────────────────────────────────────────────────────────────

class PageLoadTimeoutError(FrameworkError):
    """Raised when a page does not finish loading within the timeout."""

    def __init__(self, url: str, timeout: int = 30) -> None:
        self.url = url
        self.timeout = timeout
        super().__init__(
            f"Page '{url}' did not load within {timeout}s",
            details={"url": url, "timeout": timeout},
        )


class PageNotLoadedError(FrameworkError):
    """Raised when a page fails its readiness check (e.g. missing title / marker element)."""

    def __init__(self, page_name: str, reason: str = "") -> None:
        msg = f"Page '{page_name}' is not in the expected state"
        if reason:
            msg += f": {reason}"
        super().__init__(msg, details={"page": page_name, "reason": reason})


class InvalidURLError(FrameworkError):
    """Raised when the current URL does not match the expected pattern."""

    def __init__(self, expected: str, actual: str) -> None:
        super().__init__(
            f"URL mismatch — expected pattern '{expected}', got '{actual}'",
            details={"expected": expected, "actual": actual},
        )


# ──────────────────────────────────────────────────────────────
# Configuration / Environment Errors
# ──────────────────────────────────────────────────────────────

class ConfigurationError(FrameworkError):
    """Raised when a required configuration key is missing or invalid."""

    def __init__(self, key: str, message: str = "") -> None:
        msg = f"Configuration error for key '{key}'"
        if message:
            msg += f": {message}"
        super().__init__(msg, details={"key": key})


class EnvironmentNotFoundError(FrameworkError):
    """Raised when the requested environment config file does not exist."""

    def __init__(self, env_name: str) -> None:
        super().__init__(
            f"Environment config '{env_name}' not found in config/",
            details={"environment": env_name},
        )


# ──────────────────────────────────────────────────────────────
# Driver / Browser Errors
# ──────────────────────────────────────────────────────────────

class BrowserNotSupportedError(FrameworkError):
    """Raised when an unsupported browser is requested."""

    def __init__(self, browser_name: str) -> None:
        supported = ["chrome", "firefox", "edge"]
        super().__init__(
            f"Browser '{browser_name}' is not supported. Choose from: {supported}",
            details={"requested": browser_name, "supported": supported},
        )


class DriverInitializationError(FrameworkError):
    """Raised when the WebDriver cannot be initialized."""

    def __init__(self, browser_name: str, reason: str = "") -> None:
        msg = f"Failed to initialize {browser_name} driver"
        if reason:
            msg += f": {reason}"
        super().__init__(msg, details={"browser": browser_name, "reason": reason})


# ──────────────────────────────────────────────────────────────
# Test Data Errors
# ──────────────────────────────────────────────────────────────

class TestDataError(FrameworkError):
    """Raised when test data cannot be loaded or parsed."""

    def __init__(self, file_path: str, reason: str = "") -> None:
        msg = f"Failed to load test data from '{file_path}'"
        if reason:
            msg += f": {reason}"
        super().__init__(msg, details={"file": file_path, "reason": reason})


# ──────────────────────────────────────────────────────────────
# API / Integration Errors
# ──────────────────────────────────────────────────────────────

class APIRequestError(FrameworkError):
    """Raised when an API request used for test setup/teardown fails."""

    def __init__(
        self, method: str, url: str, status_code: int | None = None, reason: str = ""
    ) -> None:
        msg = f"API {method.upper()} {url} failed"
        if status_code:
            msg += f" with status {status_code}"
        if reason:
            msg += f": {reason}"
        super().__init__(
            msg,
            details={
                "method": method,
                "url": url,
                "status_code": status_code,
                "reason": reason,
            },
        )
