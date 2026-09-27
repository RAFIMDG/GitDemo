"""
Login Tests
===========
Tests for SauceDemo login functionality using page object fixtures.
Data-driven negative tests via external JSON data.
"""

import allure
import pytest

from utils.data_loader import DataLoader

# Load test data from data/login_data.json
_invalid_params, _invalid_ids = DataLoader.parametrize_json_with_ids(
    "login_data.json",
    key="invalid_credentials",
    fields=["username", "password", "expected_error"],
    id_field="id",
)


@allure.feature("Authentication")
@allure.story("Valid Login")
class TestValidLogin:
    """Tests for successful login scenarios."""

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_standard_user_login(self, login_page, products_page):
        """Verify standard user can login successfully."""
        login_page.login_as_standard_user()
        assert products_page.is_page_loaded(), "Products page did not load after login"

    @pytest.mark.login
    def test_login_redirects_to_inventory(self, login_page):
        """Verify login redirects to inventory page."""
        login_page.login_as_standard_user()
        assert "/inventory" in login_page.current_url


@allure.feature("Authentication")
@allure.story("Invalid Login")
class TestInvalidLogin:
    """Data-driven tests for invalid login scenarios."""

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "username,password,expected_error",
        _invalid_params,
        ids=_invalid_ids,
    )
    def test_invalid_login(self, login_page, username, password, expected_error):
        """Verify proper error message for invalid credentials."""
        login_page.login(username, password)
        error_msg = login_page.get_error_message()
        assert expected_error in error_msg, (
            f"Expected '{expected_error}' in '{error_msg}'"
        )

    @pytest.mark.login
    @pytest.mark.negative
    def test_locked_out_user_shows_error(self, login_page):
        """Verify locked out user sees appropriate error."""
        login_page.login("locked_out_user", "secret_sauce")
        assert login_page.is_login_error_displayed()
        assert "locked out" in login_page.get_error_message().lower()
