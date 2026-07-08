import os
import dotenv
import requests

dotenv.load_dotenv()

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ["SERPAPI_API_KEY"]

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):

        response = requests.get(url="https://serpapi.com/search", params=
            {
                "engine": "google_flights",
                "departure_id": origin_city_code,
                "arrival_id": destination_city_code,
                "outbound_date": from_time,
                "return_date": to_time,
                "type": "1",
                "adults": "1",
                "currency": "GBP",
                "api_key": self._api_key,
            }
        )

        response.raise_for_status()
        data = response.json()

        return data

    pass

