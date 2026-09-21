"""
Logging Utility
===============
Centralized logging configuration with both file and console handlers.
Creates a per-test-run log file and supports structured output.

Usage:
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Test started")
"""

from __future__ import annotations

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── Constants ──────────────────────────────────────────────────
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)-30s | %(funcName)-20s | %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)


def _create_file_handler(log_file: Path) -> logging.FileHandler:
    """Create a file handler with the standard formatter."""
    handler = logging.FileHandler(str(log_file), mode="a", encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    return handler


def _create_console_handler() -> logging.StreamHandler:
    """Create a console handler with coloured-level output."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    return handler


def get_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.DEBUG,
) -> logging.Logger:
    """
    Return a configured logger instance.

    Args:
        name:     Logger name (usually ``__name__``).
        log_file: Optional custom log filename (defaults to ``automation.log``).
        level:    Root level for this logger (default: ``DEBUG``).

    Returns:
        Configured ``logging.Logger`` instance with file + console handlers.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    # File handler — captures everything (DEBUG+)
    if log_file is None:
        log_file = "automation.log"
    file_path = LOG_DIR / log_file
    logger.addHandler(_create_file_handler(file_path))

    # Console handler — INFO+ for readability
    logger.addHandler(_create_console_handler())

    return logger


def get_test_logger(test_name: str) -> logging.Logger:
    """
    Create a logger that writes to a *per-test* log file.

    Useful inside fixtures to capture isolated logs per test case.

    Args:
        test_name: The ``request.node.name`` from pytest.

    Returns:
        Logger writing to ``logs/<test_name>_<timestamp>.log``.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = test_name.replace("/", "_").replace("::", "_")
    log_filename = f"{safe_name}_{timestamp}.log"

    logger = logging.getLogger(f"test.{safe_name}")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # Avoid duplicates on re-entry
    if not logger.handlers:
        logger.addHandler(_create_file_handler(LOG_DIR / log_filename))
        logger.addHandler(_create_console_handler())

    return logger
