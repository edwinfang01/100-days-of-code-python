import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

FORMS_URL = "https://forms.gle/bnVnVni3vYbg5q35A"
ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(ZILLOW_CLONE_URL)
soup = BeautifulSoup(response.text, 'html.parser')

properties = soup.select("ul[class^='List-c11n-8-84-3'] > li")
property_links = [apartment.select_one("a.property-card-link").get("href") for apartment in properties]
property_prices = [apartment.select_one("span[data-test='property-card-price']").text.strip("+/mo").strip("+ 1bd") for apartment in properties]
property_addresses = [" ".join(apartment.select_one("address[data-test='property-card-addr']").text.replace("|", "").split()) for apartment in properties]

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

def wait_for_element(criteria: tuple[str, str], timeout=5):
    wait = WebDriverWait(driver=driver, timeout=timeout)
    return wait.until(EC.visibility_of_element_located(criteria))

driver.get(FORMS_URL)

for index, apartment in enumerate(properties):
    wait_for_element((By.XPATH, "//*[@role='list']"))
    questions = driver.find_elements(By.XPATH, "//div[@role='listitem']")
    time.sleep(0.5)
    questions[0].find_element(By.XPATH, ".//*[@type='text']").send_keys(property_addresses[index])
    questions[1].find_element(By.XPATH, ".//*[@type='text']").send_keys(property_prices[index])
    questions[2].find_element(By.XPATH, ".//*[@type='text']").send_keys(property_links[index])
    driver.find_element(By.XPATH, "//div[@role='button' and contains(., 'Enviar')]").click()
    wait_for_element((By.XPATH, "//a[text()='Enviar otra respuesta']")).click()