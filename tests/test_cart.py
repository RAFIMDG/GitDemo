"""
Cart Page Test Suite
====================
Tests for the SauceDemo shopping cart functionality.

Markers: @cart, @regression
"""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.products_page import ProductsPage
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.epic("Shopping")
@allure.feature("Cart")
class TestCart:
    """Shopping cart test cases."""

    @allure.story("Cart Display")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_page_loads(self, logged_in_driver):
        """Verify the cart page loads correctly."""
        products = ProductsPage(logged_in_driver)
        products.go_to_cart()

        cart = CartPage(logged_in_driver)
        assert cart.is_page_loaded()
        assert cart.get_page_title() == "Your Cart"

    @allure.story("Cart Display")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_empty_cart(self, logged_in_driver):
        """Verify empty cart shows no items."""
        products = ProductsPage(logged_in_driver)
        products.go_to_cart()

        cart = CartPage(logged_in_driver)
        assert cart.is_cart_empty()

    @allure.story("Cart Items")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.cart
    @pytest.mark.regression
    def test_added_item_appears_in_cart(self, logged_in_driver):
        """Verify an item added from products appears in the cart."""
        products = ProductsPage(logged_in_driver)
        products.add_product_to_cart_by_name("Sauce Labs Backpack")
        products.go_to_cart()

        cart = CartPage(logged_in_driver)
        assert cart.is_item_in_cart("Sauce Labs Backpack")
        assert cart.get_cart_item_count() == 1

    @allure.story("Cart Items")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    @pytest.mark.regression
    def test_multiple_items_in_cart(self, logged_in_driver):
        """Verify multiple items can be added to the cart."""
        products = ProductsPage(logged_in_driver)
        products.add_product_to_cart_by_name("Sauce Labs Backpack")
        products.add_product_to_cart_by_name("Sauce Labs Bolt T-Shirt")
        products.go_to_cart()

        cart = CartPage(logged_in_driver)
        names = cart.get_cart_item_names()
        assert "Sauce Labs Backpack" in names
        assert "Sauce Labs Bolt T-Shirt" in names
        assert cart.get_cart_item_count() == 2

    @allure.story("Remove Items")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    @pytest.mark.regression
    def test_remove_item_from_cart(self, logged_in_driver):
        """Verify an item can be removed from the cart."""
        products = ProductsPage(logged_in_driver)
        products.add_product_to_cart_by_name("Sauce Labs Backpack")
        products.go_to_cart()

        cart = CartPage(logged_in_driver)
        cart.remove_item_by_name("Sauce Labs Backpack")
        assert cart.is_cart_empty()

    @allure.story("Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_continue_shopping_returns_to_products(self, logged_in_driver):
        """Verify 'Continue Shopping' navigates back to products."""
        products = ProductsPage(logged_in_driver)
        products.go_to_cart()

        cart = CartPage(logged_in_driver)
        cart.continue_shopping()
        assert "inventory" in logged_in_driver.current_url

    @allure.story("Navigation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.cart
    def test_checkout_navigates_to_checkout(self, logged_in_driver):
        """Verify 'Checkout' navigates to checkout step one."""
        products = ProductsPage(logged_in_driver)
        products.add_product_to_cart_by_name("Sauce Labs Backpack")
        products.go_to_cart()

        cart = CartPage(logged_in_driver)
        cart.proceed_to_checkout()
        assert "checkout-step-one" in logged_in_driver.current_url
