"""
Cart Page Object
================
Encapsulates all interactions with the SauceDemo shopping cart page.

URL: https://www.saucedemo.com/cart.html
"""

from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    """Page object for the SauceDemo cart page."""

    # ═══════════════════════════════════════════════════════════
    # LOCATORS
    # ═══════════════════════════════════════════════════════════
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_QUANTITIES = (By.CLASS_NAME, "cart_quantity")
    ITEM_DESCRIPTIONS = (By.CLASS_NAME, "inventory_item_desc")
    REMOVE_BUTTONS = (By.XPATH, "//button[contains(text(), 'Remove')]")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    CHECKOUT_BTN = (By.ID, "checkout")

    # ═══════════════════════════════════════════════════════════
    # PAGE VALIDATION
    # ═══════════════════════════════════════════════════════════
    def is_page_loaded(self) -> bool:
        """Verify cart page is displayed."""
        return self.is_element_displayed(self.PAGE_TITLE)

    @allure.step("Get cart page title")
    def get_page_title(self) -> str:
        """Return page title (should be 'Your Cart')."""
        return self.get_text(self.PAGE_TITLE)

    # ═══════════════════════════════════════════════════════════
    # CART QUERIES
    # ═══════════════════════════════════════════════════════════
    @allure.step("Get all item names in cart")
    def get_cart_item_names(self) -> list[str]:
        """Return names of all items in the cart."""
        return self.get_elements_text(self.ITEM_NAMES)

    @allure.step("Get all item prices in cart")
    def get_cart_item_prices(self) -> list[str]:
        """Return prices of all items in the cart."""
        return self.get_elements_text(self.ITEM_PRICES)

    def get_cart_item_count(self) -> int:
        """Return the number of items in the cart."""
        return self.get_element_count(self.CART_ITEMS)

    def is_item_in_cart(self, product_name: str) -> bool:
        """Check if a specific product is in the cart."""
        return product_name in self.get_cart_item_names()

    def is_cart_empty(self) -> bool:
        """Check if the cart has no items."""
        return self.get_cart_item_count() == 0

    # ═══════════════════════════════════════════════════════════
    # ACTIONS
    # ═══════════════════════════════════════════════════════════
    @allure.step("Remove item #{index} from cart")
    def remove_item_by_index(self, index: int = 0) -> None:
        """Remove an item from the cart by its position."""
        buttons = self.get_elements(self.REMOVE_BUTTONS)
        if index < len(buttons):
            buttons[index].click()
            logger.info("Removed item at index %d from cart", index)

    @allure.step("Remove '{product_name}' from cart")
    def remove_item_by_name(self, product_name: str) -> None:
        """Remove a specific product from the cart."""
        button_id = "remove-" + product_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        locator = (By.ID, button_id)
        self.click(locator)
        logger.info("Removed '%s' from cart", product_name)

    @allure.step("Click Continue Shopping")
    def continue_shopping(self) -> None:
        """Navigate back to the products page."""
        self.click(self.CONTINUE_SHOPPING_BTN)

    @allure.step("Click Checkout")
    def proceed_to_checkout(self) -> None:
        """Navigate to the checkout step-one page."""
        self.click(self.CHECKOUT_BTN)
        logger.info("Proceeding to checkout")
