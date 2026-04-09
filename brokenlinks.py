from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

driver = webdriver.Firefox()
driver.get("https://testpages.eviltester.com/")
driver.implicitly_wait(10)

links = driver.find_elements(By.TAG_NAME, "a")
print(f"Total links found: {len(links)}")

unique_urls = set()

for link in links:
    url = link.get_attribute("href")

    if url and url.startswith("http"):
        unique_urls.add(url)

print(f"Unique URLs to check: {len(unique_urls)}\n")

headers = {"User-Agent":
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:148.0) Gecko/20100101 Firefox/148.0"
}

for url in unique_urls:
    try:
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code >= 400:
            print(f"❌ Broken link: {url} -> {response.status_code}")
        else:
            print(f"✅ Valid link: {url} -> {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error: {url} -> {e}")

driver.quit()