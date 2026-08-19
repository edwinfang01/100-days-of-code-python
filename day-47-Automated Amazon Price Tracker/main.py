import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from smtplib import SMTP
import requests_cache

requests_cache.install_cache(
    "product_info_cache",
    urls_expire_after={
        "*": 3600
    }
)

URL = "https://www.amazon.com/dp/B075CYMYK6?lv=shuf&_encoding=UTF8&channelId=751&plpRedirect=mhFallback"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,en-IN;q=0.8"
}

cookies = {
    "i18n-prefs": "USD",
    "lc-main": "en_US"
}

response = requests.get(URL, headers=headers, cookies=cookies)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify())
#
price = float( soup.find(name='span', class_="a-price-whole").text + soup.find(name='span', class_="a-price-fraction").text )
product_title = " ".join(soup.find(name='span', id="productTitle").text.split())

load_dotenv()
SMTP_SERVER = os.environ['SMTP_SERVER']
MY_EMAIL = os.environ['MY_EMAIL']
MY_PASSWORD = os.environ['MY_PASSWORD']

if price < 100:
    with SMTP(SMTP_SERVER) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{product_title} is now ${price}\n{URL}".encode("utf-8")
        )

print(f"Price: {price if price else 'Not found'}")