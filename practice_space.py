# import pytest
#
# @pytest.mark.parametrize("x,y,z",[
#     (1, 2, 3),
#     (4, 5, 9),
#     (4, 2, 6),
# ])
# def test(x,y,z):
#     print(x,y,z)
#     assert x+y == z
#
# a = [3, 4, 5, 6, 7, 8, 9]
# res = list(map(lambda x: "Even" if x % 2 == 0 else "Odd", a))
#
# print(res)
# import time
#
# from selenium import webdriver
# from selenium.webdriver.common.devtools.v148.network import set_cookie
#
# # Initialize driver
# driver = webdriver.Chrome()
# driver.get("https://www.amazon.in/")
#
# # Fetch actual session capabilities
# caps = driver.capabilities
#
# # Print the full dictionary
# # print(caps)
# time.sleep(10)
#
# my_cookie = {
#     'name': 'rafi',
#     'value': '123456'# Optional: only sends cookie over HTTPS
# }
# # Access a specific capability safely
# # browser_name = caps.get('browserName')
# # browser_version = caps.get('browserVersion')
# # print(browser_name)
# # print(browser_version)
# cookies = driver.get_cookies()
# print(len(cookies))
# driver.add_cookie(my_cookie)
# update_cookie = driver.get_cookies()
# print(len(update_cookie))
# driver.delete_cookie("rafi")
# dell = driver.get_cookies()
# print(len(dell))
#
# driver.quit()
import time

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://amazon.in")

# Inject simple JavaScript to show a pop-up box
driver.execute_script("alert('Hello from JavaScript!');")
time.sleep(5)
