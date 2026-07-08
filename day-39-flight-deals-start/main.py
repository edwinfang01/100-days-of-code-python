#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from requests_cache import DO_NOT_CACHE, install_cache
from data_manager import DataManager
from pprint import pprint
from datetime import timedelta, datetime
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
import json
from notification_manager import NotificationManager

# Define expiration rules based on URL patterns
rules = {
    'https://serpapi.com/search': timedelta(hours=1), # Expire in 1 hour
    'https://api.sheety.co/cddab770c97795aab868c1d1a85414db/flightDeals/prices': DO_NOT_CACHE
}

install_cache(
    "flights_cache",
    urls_expire_after=rules,
)

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
pprint(sheet_data)

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = tomorrow.date() + timedelta(days=180)

flight_search = FlightSearch()

# to print it in json format so I can paste it into a json viewer
# print(json.dumps(flights, indent=4))

ORIGIN_CITY_CODE="LHR"

for destination in sheet_data:

    flights = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_CODE,
        destination_city_code=destination['iataCode'],
        from_time=tomorrow.strftime("%Y-%m-%d"),
        to_time=six_months_from_today.strftime("%Y-%m-%d")
    )

    cheapest_flight = find_cheapest_flight(data=flights, return_date=six_months_from_today.strftime("%Y-%m-%d"))
    print(f"{destination['city']} GBP {cheapest_flight.price}")

    if cheapest_flight.price !="N/A" and cheapest_flight.price < destination['lowestPrice']:
        print(f"Lower price flight found to {destination['city']}!")
        data_manager.update_lowest_price(
            row_id=destination['id'],
            new_price=cheapest_flight.price
        )

        notification_manager = NotificationManager()
        notification_manager.send_notification(
            f"Low price alert! Only £{cheapest_flight.price} to fly from {ORIGIN_CITY_CODE} to {destination['iataCode']},"
            f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}"
        )