import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Seleniumpractice.utils.config import Config
from Seleniumpractice.utils.driver_factory import get_driver

from Seleniumpractice.utils.screenshots import take_screenshot


@pytest.fixture
def driver():
    driver = get_driver()
    driver.get(Config.BASE_URL)

    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot on test failure
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            test_name = item.name
            path = take_screenshot(driver, test_name)
            print(f"\nScreenshot saved at: {path}")
