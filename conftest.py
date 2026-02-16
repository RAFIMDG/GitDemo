import pytest
import allure
from Seleniumpractice.utils.config import Config
from Seleniumpractice.utils.driver_factory import get_driver
import os
import subprocess



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
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"{item.name}_failure",
                attachment_type=allure.attachment_type.PNG
            )


def pytest_sessionfinish(session, exitstatus):
    if os.path.exists("allure-results"):
        subprocess.run(["allure", "generate", "allure-results", "-o", "allure-report", "--clean"])
