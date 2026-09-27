"""
Screenshot Utility
==================
Captures and manages screenshots for test reporting.
Integrates with Allure for automatic attachment on failure,
and provides manual capture for debugging.

Usage:
    from utils.screenshots import ScreenshotManager

    ss = ScreenshotManager(driver)
    ss.capture("login_success")                    # save to disk
    ss.capture_and_attach("after_checkout")        # save + attach to Allure
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import allure

from config.config_manager import ConfigManager
from utils.logger import get_logger

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

logger = get_logger(__name__)


class ScreenshotManager:
    """Manages screenshot capture, storage, and Allure attachment."""

    def __init__(self, driver: "WebDriver", output_dir: str | None = None) -> None:
        config = ConfigManager()
        self.driver = driver
        self.output_dir = Path(
            output_dir or config.screenshot_dir
        ).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── Core Capture ──────────────────────────────────────────
    def _generate_filename(self, name: str) -> str:
        """Generate a timestamped, filesystem-safe filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        safe_name = name.replace(" ", "_").replace("/", "_").replace("::", "_")
        return f"{safe_name}_{timestamp}.png"

    def capture(self, name: str = "screenshot") -> str | None:
        """
        Capture a screenshot and save it to disk.

        Args:
            name: Descriptive name for the screenshot.

        Returns:
            Absolute path to the saved file, or ``None`` on failure.
        """
        filename = self._generate_filename(name)
        filepath = self.output_dir / filename

        try:
            self.driver.save_screenshot(str(filepath))
            logger.info("Screenshot saved: %s", filepath)
            return str(filepath)
        except Exception as e:
            logger.error("Failed to capture screenshot '%s': %s", name, e)
            return None

    def capture_as_png(self, name: str = "screenshot") -> bytes | None:
        """
        Capture a screenshot as raw PNG bytes (for Allure attachment).

        Returns:
            PNG bytes, or ``None`` on failure.
        """
        try:
            png_bytes = self.driver.get_screenshot_as_png()
            logger.debug("Captured PNG bytes for '%s' (%d bytes)", name, len(png_bytes))
            return png_bytes
        except Exception as e:
            logger.error("Failed to capture PNG for '%s': %s", name, e)
            return None

    # ── Allure Integration ────────────────────────────────────
    def capture_and_attach(
        self,
        name: str = "screenshot",
        save_to_disk: bool = True,
    ) -> str | None:
        """
        Capture a screenshot, attach it to the Allure report, and
        optionally save to disk.

        Args:
            name:          Descriptive name.
            save_to_disk:  Also save a copy to the screenshots directory.

        Returns:
            Path to saved file (if ``save_to_disk``), else ``None``.
        """
        png_bytes = self.capture_as_png(name)
        if png_bytes:
            allure.attach(
                png_bytes,
                name=name,
                attachment_type=allure.attachment_type.PNG,
            )
            logger.info("Screenshot attached to Allure: %s", name)

        if save_to_disk:
            return self.capture(name)
        return None

    @staticmethod
    def attach_failure_screenshot(driver: "WebDriver", test_name: str) -> None:
        """
        Static method for use in pytest hooks — captures and attaches
        a failure screenshot without needing an instance.

        Args:
            driver:    WebDriver instance.
            test_name: Name of the failed test.
        """
        try:
            png_bytes = driver.get_screenshot_as_png()
            allure.attach(
                png_bytes,
                name=f"{test_name}_failure",
                attachment_type=allure.attachment_type.PNG,
            )
            logger.info("Failure screenshot attached for test: %s", test_name)
        except Exception as e:
            logger.error("Could not attach failure screenshot for %s: %s", test_name, e)

    # ── Cleanup ───────────────────────────────────────────────
    def cleanup_old_screenshots(self, max_age_hours: int = 72) -> int:
        """
        Delete screenshots older than ``max_age_hours``.

        Returns:
            Number of files deleted.
        """
        cutoff = datetime.now().timestamp() - (max_age_hours * 3600)
        deleted = 0

        for file in self.output_dir.glob("*.png"):
            if file.stat().st_mtime < cutoff:
                file.unlink()
                deleted += 1

        logger.info("Cleaned up %d old screenshots (older than %dh)", deleted, max_age_hours)
        return deleted
