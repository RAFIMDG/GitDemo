"""
Soft Assertions
===============
Collects multiple assertion failures without stopping the test.
At the end, call ``assert_all()`` to raise all collected failures.

Usage:
    from utils.soft_assert import SoftAssert

    soft = SoftAssert()
    soft.assert_equal(actual, expected, "Check title")
    soft.assert_true(condition, "Check button visible")
    soft.assert_all()  # raises if any assertion failed
"""

from __future__ import annotations

from typing import Any

from utils.logger import get_logger

logger = get_logger(__name__)


class SoftAssert:
    """Collect assertions and report all failures at once."""

    def __init__(self) -> None:
        self._failures: list[str] = []

    @property
    def failure_count(self) -> int:
        return len(self._failures)

    # ── Assertion Methods ─────────────────────────────────────
    def assert_true(self, condition: bool, message: str = "") -> None:
        """Assert that condition is True."""
        if not condition:
            msg = f"AssertTrue failed: {message}" if message else "AssertTrue failed"
            logger.warning("SOFT ASSERT FAIL: %s", msg)
            self._failures.append(msg)

    def assert_false(self, condition: bool, message: str = "") -> None:
        """Assert that condition is False."""
        if condition:
            msg = f"AssertFalse failed: {message}" if message else "AssertFalse failed"
            logger.warning("SOFT ASSERT FAIL: %s", msg)
            self._failures.append(msg)

    def assert_equal(self, actual: Any, expected: Any, message: str = "") -> None:
        """Assert that actual == expected."""
        if actual != expected:
            msg = f"AssertEqual failed: expected '{expected}', got '{actual}'"
            if message:
                msg = f"{message} — {msg}"
            logger.warning("SOFT ASSERT FAIL: %s", msg)
            self._failures.append(msg)

    def assert_not_equal(self, actual: Any, expected: Any, message: str = "") -> None:
        """Assert that actual != expected."""
        if actual == expected:
            msg = f"AssertNotEqual failed: both are '{actual}'"
            if message:
                msg = f"{message} — {msg}"
            logger.warning("SOFT ASSERT FAIL: %s", msg)
            self._failures.append(msg)

    def assert_contains(self, text: str, substring: str, message: str = "") -> None:
        """Assert that substring is in text."""
        if substring not in text:
            msg = f"AssertContains failed: '{substring}' not in '{text}'"
            if message:
                msg = f"{message} — {msg}"
            logger.warning("SOFT ASSERT FAIL: %s", msg)
            self._failures.append(msg)

    def assert_not_none(self, obj: Any, message: str = "") -> None:
        """Assert that obj is not None."""
        if obj is None:
            msg = f"AssertNotNone failed: {message}" if message else "AssertNotNone failed"
            logger.warning("SOFT ASSERT FAIL: %s", msg)
            self._failures.append(msg)

    # ── Finalize ──────────────────────────────────────────────
    def assert_all(self) -> None:
        """Raise AssertionError with all collected failures."""
        if self._failures:
            count = len(self._failures)
            report = f"\n{count} soft assertion(s) failed:\n"
            for i, fail in enumerate(self._failures, 1):
                report += f"  {i}. {fail}\n"
            logger.error(report)
            self._failures.clear()
            raise AssertionError(report)
        logger.info("All soft assertions passed")
