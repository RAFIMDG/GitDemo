from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from drivers.browser import Browser
from utils.config import Config


class FirefoxBrowser(Browser):

    def create_driver(self):

        options = FirefoxOptions()

        if Config.HEADLESS:
            options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)

        return driver