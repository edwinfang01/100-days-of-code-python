import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://ozh.github.io/cookieclicker/")

# wait for the language selection panel to load
english_button = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.ID, "langSelect-EN"))
)
english_button.click()

# wait for the cookie button to work
time.sleep(2)
cookie_button = driver.find_element(By.CSS_SELECTOR, value="button#bigCookie")

# initialize timer to stop the loop after 5 minutes
now = time.time()
timeout = now + 60*5
while time.time() < timeout:

    # buy the most expensive product every 15 seconds
    if time.time() - now >= 15:
        products = driver.find_elements(By.CSS_SELECTOR, value="#products > div.product")

        best_product = None
        # check each product from most expensive to cheapest
        for product in reversed(products):
            if "enabled" in product.get_attribute("class"):
                best_product = product
                break

        if best_product:
            best_product.click()
        # reset timer to count to 15 seconds again
        now = time.time()

    cookie_button.click()

cookies_per_sec = driver.find_element(By.ID, value="cookiesPerSecond").text
print(cookies_per_sec)

driver.quit()
