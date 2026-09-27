"""
Products Page Tests
===================
Tests for SauceDemo products/inventory page.
Uses logged_in_products_page fixture — already authenticated.
"""

import allure
import pytest


@allure.feature("Products")
@allure.story("Product Display")
class TestProductDisplay:
    """Tests for product listing and display."""

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.products
    def test_products_page_loads_after_login(self, logged_in_products_page):
        """Verify products page loads after login."""
        assert logged_in_products_page.is_page_loaded()

    @pytest.mark.products
    def test_app_logo_displayed(self, logged_in_products_page):
        """Verify the Swag Labs logo is displayed."""
        assert logged_in_products_page.get_logo_text() == "Swag Labs"

    @pytest.mark.products
    def test_page_title_is_products(self, logged_in_products_page):
        """Verify page title says Products."""
        assert logged_in_products_page.get_page_title() == "Products"

    @pytest.mark.products
    def test_six_products_displayed(self, logged_in_products_page):
        """Verify 6 products are listed."""
        assert logged_in_products_page.get_product_count() == 6

    @pytest.mark.products
    def test_first_product_name(self, logged_in_products_page):
        """Verify first product name (default sort A-Z)."""
        assert logged_in_products_page.get_first_product_name() == "Sauce Labs Backpack"


@allure.feature("Products")
@allure.story("Cart Operations")
class TestCartOperations:
    """Tests for add-to-cart functionality."""

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_product_to_cart(self, logged_in_products_page):
        """Verify adding a product increments the cart badge."""
        logged_in_products_page.add_first_product_to_cart()
        assert logged_in_products_page.get_cart_count() == 1

    @pytest.mark.cart
    def test_cart_badge_not_shown_initially(self, logged_in_products_page):
        """Verify cart badge is not shown when cart is empty."""
        assert logged_in_products_page.get_cart_count() == 0


@allure.feature("Products")
@allure.story("Sorting")
class TestProductSorting:
    """Tests for product sorting functionality."""

    @pytest.mark.products
    def test_sort_products_z_to_a(self, logged_in_products_page):
        """Verify sorting Z to A shows correct first product."""
        logged_in_products_page.sort_products("Name (Z to A)")
        names = logged_in_products_page.get_product_names()
        assert names == sorted(names, reverse=True)

    @pytest.mark.products
    def test_sort_products_price_low_high(self, logged_in_products_page):
        """Verify sorting by price low to high."""
        logged_in_products_page.sort_products("Price (low to high)")
        prices = logged_in_products_page.get_product_prices()
        numeric = [float(p.replace("$", "")) for p in prices]
        assert numeric == sorted(numeric)
