import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://ozh.github.io/cookieclicker/")

english_button = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.ID, "langSelect-EN"))
)
english_button.click()

time.sleep(2)
cookie_button = driver.find_element(By.CSS_SELECTOR, value="button#bigCookie")
now = time.time()
timeout = now + 60*5
while time.time() < timeout:
    if time.time() - now >= 5:
        n_of_cookies = int(driver.find_element(By.ID, value="cookies").text.split()[0])
        products = driver.find_elements(By.CSS_SELECTOR, value="#products > div.product")

        highest_price = 0
        highest_price_product = None
        for product in products:
            product_price = int(product.find_element(By.CSS_SELECTOR, value=".price").text.replace(",", "")) if product.find_element(By.CSS_SELECTOR, value=".price").text else 0
            if n_of_cookies > product_price > highest_price:
                highest_price = product_price
                highest_price_product = product

        if highest_price_product:
            highest_price_product.click()

        now = time.time()

    cookie_button.click()

cookies_per_sec = driver.find_element(By.ID, value="cookiesPerSecond").text
print(cookies_per_sec)