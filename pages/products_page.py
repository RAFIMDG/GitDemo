"""
Products Page Object
====================
Page object for the SauceDemo inventory/products page.
"""

from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("Products")
class ProductsPage(BasePage):
    """SauceDemo Products/Inventory Page."""

    # ===== LOCATORS =====
    HEADLINE = (By.XPATH, '//div[@class="app_logo"]')
    TITLE = (By.XPATH, '//span[@class="title"]')
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    PRODUCT_IMAGES = (By.XPATH, '//div[@class="inventory_item_img"]')
    ADD_TO_CART_BUTTONS = (By.XPATH, '//button[contains(text(), "Add to cart")]')
    REMOVE_BUTTONS = (By.XPATH, '//button[contains(text(), "Remove")]')
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU = (By.ID, "react-burgerMenu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    # ===== PAGE VERIFICATION =====
    @allure.step("Verify products page is loaded")
    def is_page_loaded(self) -> bool:
        """Check if the products page has loaded."""
        return self.is_element_displayed(self.TITLE)

    # ===== GETTERS =====
    @allure.step("Get page headline")
    def get_logo_text(self) -> str:
        """Return the app logo text."""
        return self.get_text(self.HEADLINE)

    @allure.step("Get page title")
    def get_page_title(self) -> str:
        """Return the inventory page title."""
        return self.get_text(self.TITLE)

    @allure.step("Get all product names")
    def get_product_names(self) -> list[str]:
        """Return a list of all product names."""
        return self.get_elements_text(self.PRODUCT_NAMES)

    @allure.step("Get first product name")
    def get_first_product_name(self) -> str:
        """Return the name of the first product."""
        names = self.get_product_names()
        return names[0] if names else ""

    @allure.step("Get all product prices")
    def get_product_prices(self) -> list[str]:
        """Return a list of all product prices as strings."""
        return self.get_elements_text(self.PRODUCT_PRICES)

    @allure.step("Get product count")
    def get_product_count(self) -> int:
        """Return the number of products on the page."""
        return self.get_element_count(self.PRODUCT_NAMES)

    # ===== ACTIONS =====
    @allure.step("Add first product to cart")
    def add_first_product_to_cart(self) -> None:
        """Click the first 'Add to cart' button."""
        self.click(self.ADD_TO_CART_BUTTONS)

    @allure.step("Sort products by: {option}")
    def sort_products(self, option: str) -> None:
        """Select a sorting option from the dropdown."""
        self.select_by_visible_text(self.SORT_DROPDOWN, option)

    @allure.step("Get cart badge count")
    def get_cart_count(self) -> int:
        """Return the number shown on the cart badge."""
        if self.is_element_displayed(self.CART_BADGE, timeout=2):
            return int(self.get_text(self.CART_BADGE))
        return 0

    @allure.step("Go to cart")
    def go_to_cart(self) -> None:
        """Click the cart icon."""
        self.click(self.CART_LINK)

    @allure.step("Logout")
    def logout(self) -> None:
        """Open burger menu and click logout."""
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)
