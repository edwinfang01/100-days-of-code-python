from flight_search import FlightSearch

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date


def find_cheapest_flight(data, return_date):
    if data is None or (not data.get("best_flights") and not data.get("other_flights")):
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    all_flights = data.get("best_flights", []) + data.get("other_flights", [])
    structured_flight_data = [
        FlightData(
            price=data.get('price', "N/A"), # apparently sometimes the price field is empty
            origin_airport=data['flights'][0]['departure_airport']['id'],
            destination_airport=data['flights'][0]['arrival_airport']['id'],
            out_date=data['flights'][0]['departure_airport']['time'].split(" ")[0],
            return_date=return_date
        )
        for data in all_flights
    ]

    cheapest_flight: FlightData = structured_flight_data[0]
    cheapest_price: int = cheapest_flight.price
    for flight in structured_flight_data:
        price = flight.price
        if price and price < cheapest_price: # apparently the price field is sometimes empty
            cheapest_price = price
            cheapest_flight = flight

    return cheapest_flight