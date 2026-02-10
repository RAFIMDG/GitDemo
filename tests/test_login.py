from Seleniumpractice.pages.login_page import LoginPage


def test_valid_login(driver):
    login = LoginPage(driver)
    login.login_as_standard_user()


def test_invalid_login(driver):
    login = LoginPage(driver)
    login.login("wrong_user", "wrong_pass")

    assert "Username and password do not match" in login.get_error_message()
