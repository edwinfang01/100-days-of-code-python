from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

PROMISED_DOWN = 100
PROMISED_UP = 100
Y_EMAIL = os.environ["Y_EMAIL"]
Y_PASSWORD = os.environ["Y_PASSWORD"]
Y_LOGIN_URL = "https://app.100daysofpython.dev/services/y/login"

class InternetSpeedTwitterBot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(Y_LOGIN_URL)
        self.up = PROMISED_UP
        self.down = PROMISED_DOWN

        self.wait_for_element((By.ID, "email")).send_keys(Y_EMAIL)
        self.wait_for_element((By.ID, "password")).send_keys(Y_PASSWORD)
        self.wait_for_element((By.ID, "password")).send_keys(Keys.ENTER)

    def wait_for_element(self, criteria: tuple[str, str], timeout=5):
        wait = WebDriverWait(driver=self.driver, timeout=timeout)
        return wait.until(EC.element_to_be_clickable(criteria))


    def get_internet_speed(self) -> tuple[float, float]:
        self.driver.get("https://www.speedtest.net/")
        self.wait_for_element((By.CSS_SELECTOR, "button[aria-label^='start speed test'")).click()
        self.wait_for_element((By.XPATH, "//p[text()='Download']/../h3[text()='—']"))
        download_speed = self.wait_for_element((By.XPATH, "//p[text()='Download']/../h3[not(text()='—')]"), timeout=30).text
        upload_speed = self.wait_for_element((By.XPATH, "//p[text()='Upload']/../h3[not(text()='—')]"), timeout=30).text
        return float(download_speed), float(upload_speed)

    def tweet_at_provider(self, down, up):
        self.driver.get("https://app.100daysofpython.dev/services/y/home")
        self.wait_for_element((By.XPATH, "//div[@id='tweet-compose']")).send_keys(f"Hey Altice, why is my internet speed {down}down/{up}up? when i pay for {PROMISED_DOWN}down/{PROMISED_UP}up?")
        self.wait_for_element((By.XPATH, "//button[@type='submit' and @id='post-btn']")).click()

internet_speed_twitter_bot = InternetSpeedTwitterBot()
down, up = internet_speed_twitter_bot.get_internet_speed()
internet_speed_twitter_bot.tweet_at_provider(down, up)