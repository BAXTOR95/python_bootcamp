import os
import requests
import json
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta


class FlightData:
    """This class is responsible for structuring the flight data."""

    def __init__(self) -> None:
        self.ENV_PATH = Path("..", "..", ".env")
        load_dotenv(dotenv_path=self.ENV_PATH)
        self.KIWI_API_KEY = os.getenv("TEQUILA_KIWI_API_KEY")
        self.KIWI_API_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
        self.headers = {
            "apikey": self.KIWI_API_KEY,
        }
        self.date_from = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
        self.date_to = (datetime.now() + timedelta(days=240)).strftime("%d/%m/%Y")
        self.price = 0
        self.departure_city = ""
        self.departure_airport_iata_code = ""
        self.arrival_city = ""
        self.arrival_airport_iata_code = ""
        self.outbound_date = ""
        self.inbound_date = ""
        self.via_city = ""

    def save_json(self, data, name):
        """
        Save JSON data to a file.

        Args:
            data (Any): The JSON data to be saved.
            name (str): The name of the file.

        Raises:
            FileNotFoundError: If the directory does not exist and cannot be created.

        """
        # Ensure the directory exists
        directory = "data"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Now, save the file within the directory
        with open(f"{directory}/{name}", "w") as file:
            json.dump(data, file, indent=4)

    def has_flight_data(self):
        """Check if flight data is available."""
        return self.price != 0

    def has_stop_overs(self):
        """Check if flight has stop overs."""
        return self.via_city != ""

    def get_flight_prices(self, city_code: str, stop_overs=0) -> dict:
        """Get flight prices for a given city code.

        This method sends a GET request to the Tequila Kiwi API to retrieve flight prices for a given city code.

        Args:
            city_code (str): The city code to get flight prices for.
            stop_overs (int): The number of stop overs to allow.

        Returns:
            dict: A dictionary containing flight data.
        """
        params = {
            "fly_from": "ORL",
            "fly_to": city_code,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "curr": "USD",
            "max_stopovers": stop_overs,
            "selected_cabins": "M",
        }
        response = requests.get(
            url=self.KIWI_API_ENDPOINT,
            headers=self.headers,
            params=params,
        )
        response.raise_for_status()
        flight_data = response.json()
        # Check if data is empty before accessing it
        if not flight_data["data"]:
            # check if stop_overs is 0
            if stop_overs == 0:
                # if no data is available, call get_flight_prices again with stop_overs = 2
                return self.get_flight_prices(city_code, 2)
            else:
                return flight_data
        best_flight = self.get_best_prices(flight_data)
        self.price = best_flight["price"]
        self.departure_city = best_flight["cityFrom"]
        self.departure_airport_iata_code = best_flight["flyFrom"]
        self.arrival_city = best_flight["cityTo"]
        self.arrival_airport_iata_code = best_flight["flyTo"]
        self.outbound_date = best_flight["route"][0]["local_departure"].split("T")[0]
        if len(best_flight["route"]) == 4:
            self.via_city = best_flight["route"][0]["cityTo"]
            self.inbound_date = best_flight["route"][3]["local_departure"].split("T")[0]
        else:
            self.inbound_date = best_flight["route"][1]["local_departure"].split("T")[0]
        self.save_json(best_flight, f"{self.arrival_city}.json")

    def get_best_prices(self, flight_data: dict) -> dict:
        """Get the best prices from the flight data.

        This method retrieves the best prices from the flight data and returns the lowest price flight.

        Args:
            flight_data (dict): The flight data to get the best prices from.

        Returns:
            dict: A dictionary containing the lowest price flight data.
        """
        lowest_price = 0
        best_flight = {}
        for flight in flight_data["data"]:
            if lowest_price == 0 or flight["price"] < lowest_price:
                lowest_price = flight["price"]
                best_flight = flight
        return best_flight
