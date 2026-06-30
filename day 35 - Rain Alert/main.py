import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
OWM_token = os.environ.get('OWM_TOKEN')
my_phone_number = os.environ.get('MY_PHONE_NUMBER')


OWM_endpoint = 'https://api.openweathermap.org/data/2.5/forecast'
weather_params = {
    'lat': 18.486057,
    'lon': -69.931213,
    'appid': OWM_token,
    'cnt': 4
}

response = requests.get(url=OWM_endpoint, params=weather_params)
response.raise_for_status()

data = response.json()
time_stamps = data['list']

condition_codes = [time_stamp['weather'][0]['id'] for time_stamp in time_stamps]

print(condition_codes)

for time_stamp in time_stamps:
    weather_id = time_stamp['weather'][0]['id']
    if weather_id < 700:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella!",
        from_="whatsapp:+14155238886",
        to=f"whatsapp:{my_phone_number}",
        )

        print(message.status)

        break
