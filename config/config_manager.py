"""
Configuration Manager
=====================
Loads environment-specific YAML config files (qa.yaml, staging.yaml, prod.yaml)
and merges them with environment variables and .env overrides.

Priority (highest → lowest):
    1. Environment variables / .env
    2. YAML config file values
    3. Hard-coded defaults

Usage:
    from config.config_manager import ConfigManager

    config = ConfigManager()              # reads ENV var or defaults to "qa"
    config = ConfigManager(env="staging")  # explicit environment

    config.base_url       # "https://www.saucedemo.com/"
    config.browser         # "chrome"
    config.get("timeouts.explicit")  # 10
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

import yaml
from dotenv import load_dotenv

from utils.exceptions import ConfigurationError, EnvironmentNotFoundError
from utils.logger import get_logger

logger = get_logger(__name__)

# Load .env from project root (if present)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


class ConfigManager:
    """Thread-safe, singleton-style configuration manager."""

    _instance: Optional["ConfigManager"] = None
    _config: dict[str, Any] = {}

    # ── Construction ──────────────────────────────────────────
    def __new__(cls, env: Optional[str] = None) -> "ConfigManager":
        """Singleton: re-create only when *env* changes."""
        target_env = (env or os.getenv("ENV", "qa")).lower()
        if cls._instance is None or cls._instance._env != target_env:
            instance = super().__new__(cls)
            instance._env = target_env
            instance._load(target_env)
            cls._instance = instance
        return cls._instance

    # ── YAML Loading ──────────────────────────────────────────
    def _load(self, env: str) -> None:
        config_dir = Path(__file__).resolve().parent
        config_file = config_dir / f"{env}.yaml"

        if not config_file.exists():
            raise EnvironmentNotFoundError(env)

        with open(config_file, "r") as f:
            self._config = yaml.safe_load(f) or {}

        logger.info("Loaded config for environment: %s", env)

    # ── Property Accessors ────────────────────────────────────
    @property
    def env(self) -> str:
        return self._env

    @property
    def base_url(self) -> str:
        return os.getenv("BASE_URL", self._config.get("base_url", ""))

    @property
    def browser(self) -> str:
        return os.getenv("BROWSER", self._config.get("browser", "chrome")).lower()

    @property
    def headless(self) -> bool:
        env_val = os.getenv("HEADLESS", "").lower()
        if env_val in ("true", "1", "yes"):
            return True
        if env_val in ("false", "0", "no"):
            return False
        return self._config.get("headless", False)

    @property
    def implicit_wait(self) -> int:
        return int(os.getenv("IMPLICIT_WAIT", self._config.get("timeouts", {}).get("implicit", 5)))

    @property
    def explicit_wait(self) -> int:
        return int(os.getenv("EXPLICIT_WAIT", self._config.get("timeouts", {}).get("explicit", 10)))

    @property
    def page_load_timeout(self) -> int:
        return int(os.getenv("PAGE_LOAD_TIMEOUT", self._config.get("timeouts", {}).get("page_load", 30)))

    @property
    def username(self) -> str:
        return os.getenv("APP_USERNAME", self._config.get("credentials", {}).get("username", ""))

    @property
    def password(self) -> str:
        return os.getenv("APP_PASSWORD", self._config.get("credentials", {}).get("password", ""))

    @property
    def screenshot_dir(self) -> str:
        return self._config.get("paths", {}).get("screenshots", "reports/screenshots")

    @property
    def log_level(self) -> str:
        return os.getenv("LOG_LEVEL", self._config.get("logging", {}).get("level", "DEBUG"))

    @property
    def selenium_grid_url(self) -> str | None:
        return os.getenv("GRID_URL", self._config.get("grid", {}).get("url"))

    @property
    def retry_count(self) -> int:
        return int(os.getenv("RETRY_COUNT", self._config.get("retry", {}).get("count", 1)))

    @property
    def retry_delay(self) -> int:
        return int(os.getenv("RETRY_DELAY", self._config.get("retry", {}).get("delay", 2)))

    # ── Generic Getter ────────────────────────────────────────
    def get(self, dotted_key: str, default: Any = None) -> Any:
        """
        Access nested config via dot notation.

        Example:
            config.get("timeouts.explicit")  →  10
        """
        keys = dotted_key.split(".")
        value: Any = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
            if value is None:
                return default
        return value

    # ── Representation ────────────────────────────────────────
    def __repr__(self) -> str:
        return f"<ConfigManager env={self._env!r} base_url={self.base_url!r}>"
