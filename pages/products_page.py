from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import Config



class ProductsPage(BasePage):

    HEADLINE = (By.XPATH, '//div[@class="app_logo"]')
    PRODUCTS_TITLES = (By.XPATH, '(//div[@class="inventory_item_name"])[1]')
    IMG = (By.XPATH, '//div[@class="inventory_item_img"]')
    ADD_TO_CART = (By.XPATH, '(//button[contains(text() ,"Add to cart")])[1]')


    def verifylogo(self):
        return self.get_text(self.HEADLINE)

    def verifyproducts(self):
        return self.get_text(self.PRODUCTS_TITLES)

    def verifyimg(self):
        return self.get_text(self.IMG)

    def verifyaddtocart(self):
        return self.get_text(self.ADD_TO_CART)


