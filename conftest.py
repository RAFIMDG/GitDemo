import pytest
import allure
from utils.config import Config
from utils.driver_factory import get_driver
import os
import subprocess



@pytest.fixture
def driver():
    driver = get_driver()
    driver.get(Config.BASE_URL)
    driver.maximize_window()

    yield driver
    driver.quit()



@pytest.fixture
def login(driver):
    def do_login(username, password):
        driver.find_element("id", "user-name").send_keys(username)
        driver.find_element("id", "password").send_keys(password)
        driver.find_element("id", "login-button").click()
        return driver

    return do_login


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
        subprocess.run([
            "/Users/grrafi/.jenkins/tools/ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation/allure/bin/allure",
            "generate", "allure-results", "-o", "allure-report", "--clean"
        ])

