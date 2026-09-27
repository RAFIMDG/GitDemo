# ==============================capturing broken links from the website ===============================

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import requests
#
# driver = webdriver.Firefox()
# driver.get("https://testpages.eviltester.com/")
# driver.implicitly_wait(10)
#
# links = driver.find_elements(By.TAG_NAME, "a")
# print(f"Total links found: {len(links)}")
#
# unique_urls = set()
#
# for link in links:
#     url = link.get_attribute("href")
#
#     if url and url.startswith("http"):
#         unique_urls.add(url)
#
# print(f"Unique URLs to check: {len(unique_urls)}\n")
#
# headers = {"User-Agent":
# 	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:148.0) Gecko/20100101 Firefox/148.0"
# }
#
# for url in unique_urls:
#     try:
#         response = requests.get(url, headers=headers, timeout=5)
#         if response.status_code >= 400:
#             print(f"❌ Broken link: {url} -> {response.status_code}")
#         else:
#             print(f"✅ Valid link: {url} -> {response.status_code}")
#
#     except requests.exceptions.RequestException as e:
#         print(f"⚠️ Error: {url} -> {e}")
#
# driver.quit()


# ======================================Capturing live net speed from fast .com =========================================
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 1. Setup Chrome options for an optimized, clean output
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Run invisibly in the background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")   # Suppress terminal warnings/logs

# 2. Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    print("Connecting to Fast.com and starting the speed test...")
    driver.get("https://fast.com/")

    # Give the page a quick second to initialize its dynamic trackers
    time.sleep(2)

    print("\nLive Tracking Speed:")
    print("-" * 25)

    while True:
        try:
            # Locate the current speed numerical value and unit (e.g., Mbps / Kbps)
            speed_element = driver.find_element(By.ID, "speed-value")
            unit_element = driver.find_element(By.ID, "speed-units")

            speed_value = speed_element.text.strip()
            speed_unit = unit_element.text.strip()

            # Print the live updates on the exact same terminal line using '\r'
            if speed_value:
                print(f"{speed_value} and {speed_unit}")
                # sys.stdout.write(f"\rCurrent Speed: {speed_value} {speed_unit}   ")
                # sys.stdout.flush()

            # Check if the speed test has concluded by looking for the "succeeded" confirmation class
            # Alternatively, if the refresh/show more section becomes active, it's done.
            container = driver.find_element(By.ID, "speed-progress-indicator")
            if "succeeded" in container.get_attribute("class"):
                print(f"\n\n✅ Final Speed Test Complete: {speed_value} {speed_unit}")
                break

        except Exception:
            # Gracefully handle occasional stale DOM elements while the layout updates live
            continue

        time.sleep(0.2)  # Update speed tracking 5 times a second

finally:
    # 3. Always close the browser instance safely
    driver.quit()
