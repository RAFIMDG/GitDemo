"""
Checkout Page Objects
=====================
Encapsulates both checkout steps and the completion page.

URLs:
  - Step One:  /checkout-step-one.html
  - Step Two:  /checkout-step-two.html
  - Complete:  /checkout-complete.html
"""

from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class CheckoutStepOnePage(BasePage):
    """Checkout Step One — shipping information."""

    # ═══════════════════════════════════════════════════════════
    # LOCATORS
    # ═══════════════════════════════════════════════════════════
    PAGE_TITLE = (By.CLASS_NAME, "title")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    ZIP_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    CANCEL_BTN = (By.ID, "cancel")
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test='error']")

    # ═══════════════════════════════════════════════════════════
    # ACTIONS
    # ═══════════════════════════════════════════════════════════
    @allure.step("Fill shipping info: {first_name} {last_name}, {zip_code}")
    def fill_shipping_info(
        self, first_name: str, last_name: str, zip_code: str
    ) -> None:
        """Fill out the checkout form fields."""
        logger.info("Filling shipping: %s %s, %s", first_name, last_name, zip_code)
        self.type(self.FIRST_NAME_INPUT, first_name)
        self.type(self.LAST_NAME_INPUT, last_name)
        self.type(self.ZIP_CODE_INPUT, zip_code)

    @allure.step("Click Continue")
    def click_continue(self) -> None:
        """Submit the shipping form."""
        self.click(self.CONTINUE_BTN)

    @allure.step("Click Cancel")
    def click_cancel(self) -> None:
        """Cancel checkout and return to cart."""
        self.click(self.CANCEL_BTN)

    def fill_and_continue(
        self, first_name: str, last_name: str, zip_code: str
    ) -> None:
        """Fill the form and proceed to step two."""
        self.fill_shipping_info(first_name, last_name, zip_code)
        self.click_continue()

    # ═══════════════════════════════════════════════════════════
    # VALIDATIONS
    # ═══════════════════════════════════════════════════════════
    def get_error_message(self) -> str:
        """Return the checkout error message text."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Check if an error is shown."""
        return self.is_element_displayed(self.ERROR_MESSAGE)

    def is_page_loaded(self) -> bool:
        return self.is_element_displayed(self.PAGE_TITLE)


class CheckoutStepTwoPage(BasePage):
    """Checkout Step Two — order review."""

    # ═══════════════════════════════════════════════════════════
    # LOCATORS
    # ═══════════════════════════════════════════════════════════
    PAGE_TITLE = (By.CLASS_NAME, "title")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_TOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_info_label.summary_total_label")
    TOTAL_PRICE = (By.CLASS_NAME, "summary_total_label")
    FINISH_BTN = (By.ID, "finish")
    CANCEL_BTN = (By.ID, "cancel")
    PAYMENT_INFO = (By.XPATH, "//div[@data-test='payment-info-value']")
    SHIPPING_INFO = (By.XPATH, "//div[@data-test='shipping-info-value']")

    # ═══════════════════════════════════════════════════════════
    # QUERIES
    # ═══════════════════════════════════════════════════════════
    @allure.step("Get order item names")
    def get_item_names(self) -> list[str]:
        return self.get_elements_text(self.ITEM_NAMES)

    @allure.step("Get order item prices")
    def get_item_prices(self) -> list[str]:
        return self.get_elements_text(self.ITEM_PRICES)

    def get_subtotal(self) -> str:
        """Return the subtotal text (e.g. 'Item total: $29.99')."""
        return self.get_text(self.ITEM_TOTAL_LABEL)

    def get_tax(self) -> str:
        """Return the tax text."""
        return self.get_text(self.TAX_LABEL)

    def get_total(self) -> str:
        """Return the total price text."""
        return self.get_text(self.TOTAL_PRICE)

    def get_payment_info(self) -> str:
        return self.get_text(self.PAYMENT_INFO)

    def get_shipping_info(self) -> str:
        return self.get_text(self.SHIPPING_INFO)

    # ═══════════════════════════════════════════════════════════
    # ACTIONS
    # ═══════════════════════════════════════════════════════════
    @allure.step("Click Finish")
    def click_finish(self) -> None:
        """Complete the order."""
        self.click(self.FINISH_BTN)
        logger.info("Order finished")

    @allure.step("Click Cancel")
    def click_cancel(self) -> None:
        """Cancel and return to products."""
        self.click(self.CANCEL_BTN)

    def is_page_loaded(self) -> bool:
        return self.is_element_displayed(self.PAGE_TITLE)


class CheckoutCompletePage(BasePage):
    """Checkout Complete — order confirmation."""

    # ═══════════════════════════════════════════════════════════
    # LOCATORS
    # ═══════════════════════════════════════════════════════════
    PAGE_TITLE = (By.CLASS_NAME, "title")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    PONY_EXPRESS_IMG = (By.CLASS_NAME, "pony_express")
    BACK_HOME_BTN = (By.ID, "back-to-products")

    # ═══════════════════════════════════════════════════════════
    # VALIDATIONS
    # ═══════════════════════════════════════════════════════════
    @allure.step("Get order confirmation header")
    def get_confirmation_header(self) -> str:
        """Return the confirmation header (e.g. 'Thank you for your order!')."""
        return self.get_text(self.COMPLETE_HEADER)

    @allure.step("Get order confirmation text")
    def get_confirmation_text(self) -> str:
        """Return the confirmation body text."""
        return self.get_text(self.COMPLETE_TEXT)

    def is_order_complete(self) -> bool:
        """Check if the order completed successfully."""
        return self.is_element_displayed(self.COMPLETE_HEADER)

    # ═══════════════════════════════════════════════════════════
    # ACTIONS
    # ═══════════════════════════════════════════════════════════
    @allure.step("Click Back Home")
    def go_back_home(self) -> None:
        """Navigate back to the products page."""
        self.click(self.BACK_HOME_BTN)

    def is_page_loaded(self) -> bool:
        return self.is_element_displayed(self.PAGE_TITLE)
