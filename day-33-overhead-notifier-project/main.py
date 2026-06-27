import time

import requests
from datetime import datetime
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

MY_LAT = 18.486057
MY_LONG = -69.931213

def iss_within_range():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])

    return MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5

def is_night():
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 0,
        'tzid': 'America/Santo_Domingo'
    }

    response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
    time_now = datetime.now().hour

    # print(f"sunrise: {sunrise}, sunset {sunset}")

    return time_now >= sunset or time_now <=sunrise


while True:
    if iss_within_range() and is_night():
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=("Subject:Look up!\n\n"
                     "The ISS is above you in the sky.")
            )
    time.sleep(60)