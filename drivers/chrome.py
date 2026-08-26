from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from drivers.browser import Browser
from utils.config import Config


class ChromeBrowser(Browser):

    def create_driver(self):

        options = ChromeOptions()

        if Config.HEADLESS:
            options.add_argument("--headless=new")

        driver = webdriver.Chrome(options=options)

        return driver