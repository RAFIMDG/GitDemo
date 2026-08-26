from drivers.chrome import ChromeBrowser
from drivers.firefox import FirefoxBrowser
from utils.config import Config


def get_driver(browser_name):

    browsers = {
        "chrome": ChromeBrowser,
        "firefox": FirefoxBrowser
    }

    browser_class = browsers.get(browser_name.lower())

    if not browser_class:
        raise ValueError(
            f"Unsupported browser: {browser_name}"
        )
    browser = browser_class()
    driver = browser.create_driver()
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()

    return driver