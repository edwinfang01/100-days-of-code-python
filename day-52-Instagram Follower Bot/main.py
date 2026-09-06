import time

from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['PASSWORD']
TARGET_ACCOUNT = 'chefsteps' # Account to follow its followers
BASE_URL = "https://www.instagram.com/"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 10)
def wait_for_element(criteria: tuple[str, str]):
    return wait.until(EC.element_to_be_clickable(criteria))

driver.get(BASE_URL)

# Login
wait_for_element((By.CSS_SELECTOR, "input[name='email']")).send_keys(EMAIL)
wait_for_element((By.CSS_SELECTOR, "input[type='password']")).send_keys(PASSWORD)
wait_for_element((By.CSS_SELECTOR, "input[type='password']")).send_keys(Keys.ENTER)
wait_for_element((By.XPATH, "//div[@role='button' and text()='Ahora no']")).click()
wait_for_element((By.XPATH, "//button[text()='Ahora no']")).click()


# Follow followers
driver.get(BASE_URL + TARGET_ACCOUNT)
wait_for_element((By.XPATH, "//a//span[contains(text(), 'seguidores')]")).click()
wait_for_element((By.XPATH, "//div[contains(text(), 'Seguidores')]")).click()
time.sleep(2)
follow_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Seguir')]")
# scrollable_div = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div")

for button in follow_buttons:
    try:
        button.click()
        print("clicked follow button")
        time.sleep(1)
    except Exception as e:
        print(f"error when clicking button: {e}")

# driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)