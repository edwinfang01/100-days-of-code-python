import time
from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get("https://app.100daysofpython.dev/services/tindog/u/dpsE5HQMuczKP0Qu2GcijfG9BFzJlsFD")

wait = WebDriverWait(driver, 5)
def wait_for_element(criteria: tuple[str, str]):
    return wait.until(EC.element_to_be_clickable(criteria))

login_button = wait_for_element((By.CSS_SELECTOR, 'button[class*="tindog-login"]'))
login_button.click()

fb_button = wait_for_element((By.XPATH, "//button[starts-with(@class, 'btn-facebark')]"))
fb_button.click()

base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)
print(driver.title)

email_input = wait_for_element((By.XPATH, "//input[@id='email']"))
email_input.send_keys("aa@a")

password_input = driver.find_element(By.XPATH, "//input[@id='pass']")
password_input.send_keys("5")
password_input.send_keys(Keys.ENTER)

driver.switch_to.window(base_window)
wait_for_element((By.XPATH, "//button[text()='Allow']")).click()
wait_for_element((By.XPATH, "//button[text()='Not interested']")).click()
wait_for_element((By.XPATH, "//button[text()='I Accept']")).click()

for i in range(20):
    try:
        wait_for_element((By.XPATH, "//button[@class='btn-like']")).click()
    except ElementClickInterceptedException:
        wait_for_element((By.XPATH, "//a[@class='match-popup-link']")).click()
    time.sleep(1)
