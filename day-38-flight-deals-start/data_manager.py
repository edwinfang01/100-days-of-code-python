import requests
import os
import dotenv
from requests.auth import HTTPBasicAuth

dotenv.load_dotenv()
SHEETY_ENDPOINT = "https://api.sheety.co/cddab770c97795aab868c1d1a85414db/flightDeals/prices"

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = (self._user, self._password)
        self.destination_data = {}

    def get_destination_data(self) -> list[dict]:
        response = requests.get(url=SHEETY_ENDPOINT, auth=self._authorization)
        self.destination_data = response.json()['prices']
        source: str = 'CACHE' if getattr(response, 'from_cache', False) else 'API'
        print(source)
        return self.destination_data

    def update_lowest_price(self, row_id, new_price):

        response = requests.put(
            url=f"{SHEETY_ENDPOINT}/{row_id}",
            json= {
                'price':{
                    'lowestPrice': new_price
                }
            },
            auth=self._authorization
        )

        response.raise_for_status()

    pass