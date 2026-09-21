"""
Data Loader Utility
===================
Loads test data from JSON, CSV, and YAML files in the ``data/`` directory.
Supports data-driven testing by converting file data into pytest-friendly formats.

Usage:
    from utils.data_loader import DataLoader

    # JSON
    login_data = DataLoader.load_json("login_data.json")

    # CSV → list of dicts
    checkout_rows = DataLoader.load_csv("checkout_data.csv")

    # YAML
    config_data = DataLoader.load_yaml("some_config.yaml")

    # Parametrize helper — returns list of tuples for @pytest.mark.parametrize
    params = DataLoader.parametrize_json(
        "login_data.json",
        key="invalid_credentials",
        fields=["username", "password", "expected_error"],
    )
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml

from utils.exceptions import TestDataError
from utils.logger import get_logger

logger = get_logger(__name__)

# Resolve the ``data/`` directory relative to project root
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class DataLoader:
    """Static helper class for loading test data files."""

    # ── JSON ──────────────────────────────────────────────────
    @staticmethod
    def load_json(filename: str, key: str | None = None) -> Any:
        """
        Load a JSON file from ``data/``.

        Args:
            filename: File name (e.g. ``"login_data.json"``).
            key:      Optional top-level key to extract.

        Returns:
            Parsed JSON data (dict / list), or a specific key's value.
        """
        file_path = _DATA_DIR / filename
        logger.debug("Loading JSON: %s", file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise TestDataError(str(file_path), "File not found")
        except json.JSONDecodeError as e:
            raise TestDataError(str(file_path), f"Invalid JSON: {e}")

        if key:
            if key not in data:
                raise TestDataError(str(file_path), f"Key '{key}' not found")
            return data[key]

        return data

    # ── CSV ───────────────────────────────────────────────────
    @staticmethod
    def load_csv(filename: str) -> list[dict[str, str]]:
        """
        Load a CSV file as a list of dictionaries (one per row).

        Args:
            filename: File name (e.g. ``"checkout_data.csv"``).

        Returns:
            List of dicts keyed by header column names.
        """
        file_path = _DATA_DIR / filename
        logger.debug("Loading CSV: %s", file_path)

        try:
            with open(file_path, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except FileNotFoundError:
            raise TestDataError(str(file_path), "File not found")
        except csv.Error as e:
            raise TestDataError(str(file_path), f"CSV parse error: {e}")

        logger.debug("Loaded %d rows from %s", len(rows), filename)
        return rows

    # ── YAML ──────────────────────────────────────────────────
    @staticmethod
    def load_yaml(filename: str, key: str | None = None) -> Any:
        """
        Load a YAML file from ``data/``.

        Args:
            filename: File name (e.g. ``"users.yaml"``).
            key:      Optional top-level key to extract.

        Returns:
            Parsed YAML data.
        """
        file_path = _DATA_DIR / filename
        logger.debug("Loading YAML: %s", file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            raise TestDataError(str(file_path), "File not found")
        except yaml.YAMLError as e:
            raise TestDataError(str(file_path), f"Invalid YAML: {e}")

        if key:
            if isinstance(data, dict) and key in data:
                return data[key]
            raise TestDataError(str(file_path), f"Key '{key}' not found")

        return data

    # ── Parametrize Helpers ───────────────────────────────────
    @staticmethod
    def parametrize_json(
        filename: str,
        key: str,
        fields: list[str],
        id_field: str | None = None,
    ) -> list[tuple]:
        """
        Build a list of tuples suitable for ``@pytest.mark.parametrize``.

        Args:
            filename:  JSON data file name.
            key:       Top-level key containing the list of test cases.
            fields:    Fields to extract from each dict into the tuple.
            id_field:  Optional field to use as the pytest test ID.

        Returns:
            List of tuples, one per test case.

        Example:
            >>> DataLoader.parametrize_json(
            ...     "login_data.json",
            ...     key="invalid_credentials",
            ...     fields=["username", "password", "expected_error"],
            ...     id_field="id",
            ... )
            [("wrong_user", "wrong_pass", "Username and password do not match"), ...]
        """
        items = DataLoader.load_json(filename, key=key)
        result = []

        for item in items:
            values = tuple(item.get(field, "") for field in fields)
            result.append(values)

        logger.debug(
            "Parametrized %d test cases from %s[%s]", len(result), filename, key
        )
        return result

    @staticmethod
    def parametrize_json_with_ids(
        filename: str,
        key: str,
        fields: list[str],
        id_field: str = "id",
    ) -> tuple[list[tuple], list[str]]:
        """
        Like ``parametrize_json`` but also returns a list of test IDs.

        Returns:
            (params, ids) — use as:
                ``@pytest.mark.parametrize("a,b,c", params, ids=ids)``
        """
        items = DataLoader.load_json(filename, key=key)
        params = []
        ids = []

        for item in items:
            values = tuple(item.get(field, "") for field in fields)
            params.append(values)
            ids.append(str(item.get(id_field, "")))

        return params, ids

    @staticmethod
    def parametrize_csv(
        filename: str,
        fields: list[str] | None = None,
        id_field: str | None = None,
    ) -> list[tuple]:
        """
        Build parametrize tuples from a CSV file.

        Args:
            filename: CSV file name.
            fields:   Columns to include (``None`` = all columns).
            id_field: Column to use as pytest test ID.

        Returns:
            List of tuples, one per CSV row.
        """
        rows = DataLoader.load_csv(filename)
        if not rows:
            return []

        if fields is None:
            fields = list(rows[0].keys())

        return [tuple(row.get(f, "") for f in fields) for row in rows]
