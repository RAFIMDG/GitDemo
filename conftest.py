"""
Root conftest.py
================
Central pytest configuration with:
- Browser CLI option
- Driver fixture with automatic teardown
- Page object fixtures (no more LoginPage(driver) in tests!)
- Allure screenshot on failure
- Allure environment info
- Logging per test
"""

import os

import allure
import pytest

from config.config_manager import ConfigManager
from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutStepOnePage, CheckoutStepTwoPage, CheckoutCompletePage
from utils.logger import get_logger, get_test_logger
from utils.screenshots import ScreenshotManager
from utils.soft_assert import SoftAssert

logger = get_logger(__name__)


# ── CLI Options ───────────────────────────────────────────────
def pytest_addoption(parser):
    """Add custom CLI options."""
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser to run tests: chrome, firefox, or edge",
    )
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Environment to test against: qa, staging, or prod",
    )


# ── Core Fixtures ─────────────────────────────────────────────
@pytest.fixture(scope="session")
def config(request):
    """Session-scoped configuration."""
    env = request.config.getoption("--env")
    return ConfigManager(env=env) if env else ConfigManager()

@pytest.fixture(params=["chrome", "firefox"])
# @pytest.fixture
def driver(request, config):
    """Create a WebDriver instance per test with automatic teardown."""
    # browser_name = request.config.getoption("--browser") or config.browser # to get the browser from configs
    browser_name = request.param # used browser_name from the fixture parameter

    logger.info("=" * 60)
    logger.info("TEST: %s", request.node.name)
    logger.info("Browser: %s | Env: %s", browser_name, config.env)
    logger.info("=" * 60)

    driver = DriverFactory.create_driver(browser_name)
    driver.get(config.base_url)

    yield driver

    driver.quit()
    logger.info("Driver closed for test: %s", request.node.name)


# ── Page Object Fixtures ─────────────────────────────────────
# These eliminate the need for "login = LoginPage(driver)" in every test!

@pytest.fixture
def login_page(driver) -> LoginPage:
    """Login page object — auto-injected into tests."""
    return LoginPage(driver)


@pytest.fixture
def products_page(driver) -> ProductsPage:
    """Products page object — auto-injected into tests."""
    return ProductsPage(driver)


@pytest.fixture
def logged_in_driver(driver):
    """Driver already logged in as standard user."""
    login = LoginPage(driver)
    login.login_as_standard_user()
    return driver


@pytest.fixture
def logged_in_products_page(logged_in_driver) -> ProductsPage:
    """Products page after successful login."""
    return ProductsPage(logged_in_driver)


@pytest.fixture
def cart_page(driver) -> CartPage:
    """Cart page object — auto-injected into tests."""
    return CartPage(driver)


@pytest.fixture
def checkout_step_one(driver) -> CheckoutStepOnePage:
    """Checkout step one page object."""
    return CheckoutStepOnePage(driver)


@pytest.fixture
def checkout_step_two(driver) -> CheckoutStepTwoPage:
    """Checkout step two page object."""
    return CheckoutStepTwoPage(driver)


@pytest.fixture
def checkout_complete(driver) -> CheckoutCompletePage:
    """Checkout complete page object."""
    return CheckoutCompletePage(driver)


# ── Utility Fixtures ──────────────────────────────────────────
@pytest.fixture
def soft_assert() -> SoftAssert:
    """Soft assertion helper — collect failures, assert at end."""
    sa = SoftAssert()
    yield sa
    sa.assert_all()


@pytest.fixture
def test_logger(request):
    """Per-test logger that writes to an isolated log file."""
    return get_test_logger(request.node.name)


# ── Hooks ─────────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure and attach to Allure."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            ScreenshotManager.attach_failure_screenshot(driver, item.name)


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression tests")
    config.addinivalue_line("markers", "login: Login-related tests")
    config.addinivalue_line("markers", "products: Product page tests")
    config.addinivalue_line("markers", "cart: Shopping cart tests")
    config.addinivalue_line("markers", "negative: Negative/error tests")
    config.addinivalue_line("markers", "checkout: Checkout flow tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")


def pytest_sessionfinish(session, exitstatus):
    """Generate Allure environment info after test run."""
    cfg = ConfigManager()
    allure_dir = "allure-results"

    if os.path.exists(allure_dir):
        env_file = os.path.join(allure_dir, "environment.properties")
        with open(env_file, "w") as f:
            f.write(f"Environment={cfg.env}\n")
            f.write(f"Browser={cfg.browser}\n")
            f.write(f"Base.URL={cfg.base_url}\n")
            f.write(f"Headless={cfg.headless}\n")
        logger.info("Allure environment.properties written")
