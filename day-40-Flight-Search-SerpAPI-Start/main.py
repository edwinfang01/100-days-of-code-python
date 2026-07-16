import requests_cache
from pprint import pprint
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager


# ==================== Conserve requests and preserve your free plan ====================
requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    }
)
# ==================== Setup ====================
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
# pprint(sheet_data)
flight_search = FlightSearch()
# Create an instance of the NotificationManager
notification_manager = NotificationManager()

# ==================== Set the Dates and Origin Airport ====================
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
ORIGIN_CITY_IATA = "LHR"  # London Heathrow

# ==================== Find Cheap Flights ====================

customer_data = data_manager.get_customer_emails()

customer_email_list = [
    customer["whatIsYourEmail?"] for customer in customer_data
]

for destination in sheet_data:
    # Search for direct flights
    pprint(f"Getting direct flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today,
    )
    cheapest_flight = find_cheapest_flight(flights, return_date=six_month_from_today.strftime("%Y-%m-%d"), )
    pprint(f"{destination['city']}: GBP {cheapest_flight.price}")

    # Search for indirect flights if no direct flights were found
    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination["iataCode"]} exists. Looking for indirect flights...")
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False
        )

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:

        if cheapest_flight.stops == 0:
            msg = f"Low price alert! Only GBP {cheapest_flight.price} to fly directly "\
                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            msg = f"Low price alert! Only GBP {cheapest_flight.price} to fly " \
                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                  f"with {cheapest_flight.stops} stop(s)"\
                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."

        pprint(f"Lower price flight found to {destination['city']}!")
        data_manager.update_lowest_price(destination["id"], cheapest_flight.price)
        # notification_manager.send_sms(
        #     message_body=f"Low price alert! Only GBP {cheapest_flight.price} to fly "
        #                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
        #                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        # )
        # SMS not working? Try whatsapp instead.
        notification_manager.send_whatsapp(
            message_body=msg
        )

        notification_manager.send_emails(
            customer_email_list,
            email_body=msg
        )