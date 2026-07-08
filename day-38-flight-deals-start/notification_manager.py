from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self._sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self._auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self._my_phone_number = os.environ.get('MY_PHONE_NUMBER')

    def send_notification(self, body):
        client = Client(self._sid, self._auth_token)
        message = client.messages.create(
            body=body,
            from_="whatsapp:+14155238886",
            to=f"whatsapp:{os.environ.get('MY_PHONE_NUMBER')}",
        )
        print(message.status)

    pass