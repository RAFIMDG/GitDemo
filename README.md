# 🚀 SauceDemo Automation Framework

A **production-grade** Selenium + Pytest automation framework built with industry best practices.

---

## 📁 Project Structure

```
GitDemo/
├── config/                     # Environment-aware YAML configuration
│   ├── config_manager.py       # Singleton config loader (YAML + .env)
│   ├── qa.yaml                 # QA environment settings
│   ├── staging.yaml            # Staging environment settings
│   └── prod.yaml               # Production environment settings
│
├── data/                       # Test data (JSON/CSV)
│   ├── login_data.json         # Login test data (valid + invalid)
│   └── products_data.json      # Product test data
│
├── drivers/                    # Browser driver factory (Strategy Pattern)
│   ├── browser.py              # Abstract base class
│   ├── chrome.py               # Chrome with stability flags
│   ├── firefox.py              # Firefox with preferences
│   ├── edge.py                 # Edge (Chromium)
│   └── driver_factory.py       # Central factory with Grid support
│
├── pages/                      # Page Object Model
│   ├── base_page.py            # 30+ reusable methods (click, type, scroll, dropdown, etc.)
│   ├── login_page.py           # Login page actions & validations
│   └── products_page.py        # Products page with sorting, cart, etc.
│
├── tests/                      # Test suites
│   ├── test_login.py           # Data-driven login tests
│   └── test_products.py        # Product display, cart, sorting tests
│
├── utils/                      # Utilities
│   ├── api_helper.py           # HTTP client for API test setup
│   ├── data_loader.py          # JSON/CSV/YAML data loader
│   ├── exceptions.py           # Custom framework exceptions
│   ├── logger.py               # File + console logging
│   ├── screenshots.py          # Screenshot capture + Allure attachment
│   ├── soft_assert.py          # Collect multiple assertion failures
│   └── waits_utils.py          # 20+ explicit wait methods
│
├── logs/                       # Auto-generated log files
├── reports/screenshots/        # Failure screenshots
├── allure-results/             # Allure raw results
├── allure-report/              # Allure HTML report
│
├── conftest.py                 # Fixtures, hooks, markers, page fixtures
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── docker-compose.yml          # Selenium Grid (Chrome + Firefox + Edge)
├── Jenkinsfile                 # Jenkins CI pipeline
└── .github/workflows/ci.yml   # GitHub Actions CI
```

---

## ⚡ Quick Start

### 1. Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run all tests
```bash
pytest
```

### 3. Run by marker
```bash
pytest -m smoke            # Smoke tests only
pytest -m login            # Login tests only
pytest -m "not negative"   # Skip negative tests
```

### 4. Run specific browser
```bash
pytest --browser=firefox
pytest --browser=edge
```

### 5. Run specific environment
```bash
pytest --env=staging
pytest --env=prod
```

### 6. Run headless
```bash
HEADLESS=true pytest
```

### 7. Parallel execution
```bash
pytest -n 4   # 4 parallel workers
```

### 8. Rerun failures
```bash
pytest --reruns 2 --reruns-delay 2
```

### 9. View Allure report
```bash
allure serve allure-results
```

---

## 🏗️ Architecture

### Design Patterns
| Pattern | Where | Why |
|---------|-------|-----|
| **Page Object Model** | `pages/` | Encapsulate UI interactions |
| **Factory Pattern** | `drivers/driver_factory.py` | Create browser drivers dynamically |
| **Strategy Pattern** | `drivers/browser.py` | Swap browser implementations |
| **Singleton** | `config/config_manager.py` | Single config instance across tests |
| **Data-Driven** | `data/` + `DataLoader` | External test data (JSON/CSV) |

### Key Features
- ✅ **Page Object Fixtures** — No more `login = LoginPage(driver)` in every test
- ✅ **YAML Config** — Multi-environment (QA/Staging/Prod) with .env overrides
- ✅ **Data-Driven Tests** — JSON/CSV test data with parametrize helper
- ✅ **Custom Exceptions** — Framework-specific error classification
- ✅ **Structured Logging** — File + console, per-test log files
- ✅ **Allure Reporting** — Steps, features, stories, severity, screenshots on failure
- ✅ **Soft Assertions** — Collect multiple failures per test
- ✅ **Cross-Browser** — Chrome, Firefox, Edge
- ✅ **Selenium Grid** — Docker Compose for parallel distributed runs
- ✅ **CI/CD** — Jenkins + GitHub Actions
- ✅ **Retry/Rerun** — Built-in flaky test handling
- ✅ **Parallel Execution** — pytest-xdist support

---

## 🐳 Selenium Grid (Docker)

```bash
# Start Grid
docker-compose up -d

# Run tests against Grid
GRID_URL=http://localhost:4444/wd/hub pytest --browser=chrome

# Stop Grid
docker-compose down
```

---

## 📊 Test Data

Test data lives in `data/` as JSON files. Use `DataLoader` in tests:

```python
from utils.data_loader import DataLoader

# Load and parametrize
params, ids = DataLoader.parametrize_json_with_ids(
    "login_data.json",
    key="invalid_credentials",
    fields=["username", "password", "expected_error"],
    id_field="id",
)

@pytest.mark.parametrize("username,password,expected", params, ids=ids)
def test_invalid_login(login_page, username, password, expected):
    login_page.login(username, password)
    assert expected in login_page.get_error_message()
```

---

## 🧪 Writing New Tests

```python
# tests/test_checkout.py
import pytest

@pytest.mark.cart
def test_checkout_flow(logged_in_products_page):
    """No need to create page objects manually — fixtures handle it!"""
    logged_in_products_page.add_first_product_to_cart()
    assert logged_in_products_page.get_cart_count() == 1
```

Available fixtures (from `conftest.py`):
- `driver` — Fresh WebDriver per test
- `login_page` — LoginPage object
- `products_page` — ProductsPage object
- `logged_in_driver` — Already authenticated driver
- `logged_in_products_page` — Products page after login
- `soft_assert` — Soft assertion helper
- `config` — Configuration manager

---

## 📝 License

Internal / Personal Project
