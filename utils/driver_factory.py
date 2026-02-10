from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from Seleniumpractice.utils.config import Config


def get_driver():
    browser = Config.BROWSER.lower()
    if browser == "chrome":
        options = ChromeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    else:
        raise Exception("Unsupported browser")

    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()
    return driver



