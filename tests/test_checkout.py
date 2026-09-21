"""
Checkout Flow Test Suite
========================
Tests for the SauceDemo checkout process (steps one, two, and complete).

Markers: @checkout, @e2e, @regression
"""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletePage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
)
from pages.products_page import ProductsPage
from utils.data_loader import DataLoader
from utils.logger import get_logger

logger = get_logger(__name__)

# ── Load checkout test data from CSV ──────────────────────────
_CHECKOUT_DATA = DataLoader.load_csv("checkout_data.csv")


@allure.epic("Shopping")
@allure.feature("Checkout")
class TestCheckout:
    """Checkout flow test cases."""

    # ── Helper: navigate to checkout step one ──────────────────
    def _navigate_to_checkout(self, driver) -> None:
        """Add a product and navigate to checkout step one."""
        products = ProductsPage(driver)
        products.add_product_to_cart_by_name("Sauce Labs Backpack")
        products.go_to_cart()

        cart = CartPage(driver)
        cart.proceed_to_checkout()

    # ══════════════════════════════════════════════════════════
    # STEP ONE — Shipping Info
    # ══════════════════════════════════════════════════════════
    @allure.story("Checkout Step One")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_checkout_step_one_loads(self, logged_in_driver):
        """Verify checkout step one page loads."""
        self._navigate_to_checkout(logged_in_driver)
        step_one = CheckoutStepOnePage(logged_in_driver)
        assert step_one.is_page_loaded()

    @allure.story("Checkout Step One")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_valid_checkout_info(self, logged_in_driver):
        """Verify valid shipping info proceeds to step two."""
        self._navigate_to_checkout(logged_in_driver)

        step_one = CheckoutStepOnePage(logged_in_driver)
        step_one.fill_and_continue("John", "Doe", "90210")
        assert "checkout-step-two" in logged_in_driver.current_url

    @allure.story("Checkout Step One — Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_checkout_empty_first_name(self, logged_in_driver):
        """Verify error when first name is empty."""
        self._navigate_to_checkout(logged_in_driver)

        step_one = CheckoutStepOnePage(logged_in_driver)
        step_one.fill_and_continue("", "Doe", "90210")
        assert step_one.is_error_displayed()
        assert "First Name is required" in step_one.get_error_message()

    @allure.story("Checkout Step One — Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_checkout_empty_last_name(self, logged_in_driver):
        """Verify error when last name is empty."""
        self._navigate_to_checkout(logged_in_driver)

        step_one = CheckoutStepOnePage(logged_in_driver)
        step_one.fill_and_continue("John", "", "90210")
        assert step_one.is_error_displayed()
        assert "Last Name is required" in step_one.get_error_message()

    @allure.story("Checkout Step One — Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_checkout_empty_zip(self, logged_in_driver):
        """Verify error when zip code is empty."""
        self._navigate_to_checkout(logged_in_driver)

        step_one = CheckoutStepOnePage(logged_in_driver)
        step_one.fill_and_continue("John", "Doe", "")
        assert step_one.is_error_displayed()
        assert "Postal Code is required" in step_one.get_error_message()

    @allure.story("Checkout Step One — Cancel")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.checkout
    def test_checkout_cancel_returns_to_cart(self, logged_in_driver):
        """Verify Cancel returns to the cart page."""
        self._navigate_to_checkout(logged_in_driver)

        step_one = CheckoutStepOnePage(logged_in_driver)
        step_one.click_cancel()
        assert "cart" in logged_in_driver.current_url

    # ══════════════════════════════════════════════════════════
    # STEP TWO — Order Review
    # ══════════════════════════════════════════════════════════
    @allure.story("Checkout Step Two")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_order_review_shows_correct_item(self, logged_in_driver):
        """Verify the order review page shows the correct product."""
        self._navigate_to_checkout(logged_in_driver)

        step_one = CheckoutStepOnePage(logged_in_driver)
        step_one.fill_and_continue("John", "Doe", "90210")

        step_two = CheckoutStepTwoPage(logged_in_driver)
        items = step_two.get_item_names()
        assert "Sauce Labs Backpack" in items

    @allure.story("Checkout Step Two")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.checkout
    def test_order_review_shows_total(self, logged_in_driver):
        """Verify the order review page shows a total price."""
        self._navigate_to_checkout(logged_in_driver)

        step_one = CheckoutStepOnePage(logged_in_driver)
        step_one.fill_and_continue("John", "Doe", "90210")

        step_two = CheckoutStepTwoPage(logged_in_driver)
        total = step_two.get_total()
        assert "Total:" in total

    # ══════════════════════════════════════════════════════════
    # END-TO-END
    # ══════════════════════════════════════════════════════════
    @allure.story("Complete Checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_complete_checkout_flow(self, logged_in_driver):
        """End-to-end: add item → cart → checkout → confirm."""
        # Add item
        products = ProductsPage(logged_in_driver)
        products.add_product_to_cart_by_name("Sauce Labs Backpack")
        products.go_to_cart()

        # Cart → Checkout
        cart = CartPage(logged_in_driver)
        cart.proceed_to_checkout()

        # Fill shipping info
        step_one = CheckoutStepOnePage(logged_in_driver)
        step_one.fill_and_continue("John", "Doe", "90210")

        # Review & Finish
        step_two = CheckoutStepTwoPage(logged_in_driver)
        step_two.click_finish()

        # Confirm
        complete = CheckoutCompletePage(logged_in_driver)
        assert complete.is_order_complete()
        assert complete.get_confirmation_header() == "Thank you for your order!"
