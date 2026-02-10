import os


class  Config:
    ENV = os.getenv("ENV","QA")


    BASE_URLS = {
        "QA": "https://www.saucedemo.com/"
    }

    BASE_URL = BASE_URLS.get(ENV)

    IMPLICIT_WAIT  = 5
    EC_WAIT_TIME = 10
    IMPLICIT_WAIT_INTERVAL = 15

    SCREENSHOT_PATH = os.path.join(os.getcwd(), "screenshot.png")

    USERNAME = os.getenv("APP_USERNAME", "standard_user")
    PASSWORD = os.getenv("APP_PASSWORD", "secret_sauce")


    BROWSER= os.getenv("BROWSE", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"