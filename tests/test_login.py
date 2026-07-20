import pytest

from pages.login_page import LoginPage


def test_valid_login(driver):
    login = LoginPage(driver)
    login.login_as_standard_user()


@pytest.mark.parametrize("username,password,expected", [
    ("wrong_user", "wrong_pass", "Username and password do not match"),
    ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
    ("standard_user", "wrong_pass", "Username and password do not match"),
    ("", "", "Epic sadface: Username is required"),
    ("standard_user", "", "Epic sadface: Password is required"),
])
def test_invalid_login(driver, username, password, expected):
    login = LoginPage(driver)
    login.login(username, password)

    assert expected in login.get_error_message()
