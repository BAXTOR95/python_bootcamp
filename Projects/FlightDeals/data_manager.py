import os
import requests
from dotenv import load_dotenv
from pathlib import Path


class DataManager:
    """This class is responsible for talking to the Google Sheet."""

    def __init__(self):
        self.sheet_data = {}
        self.ENV_PATH = Path("..", "..", ".env")
        load_dotenv(dotenv_path=self.ENV_PATH)
        self.SHEETY_FLIGHTS_ENDPOINT = os.getenv("SHEETY_FLIGHTS_ENDPOINT")
        self.SHEETY_AUTH_TOKEN = os.getenv("SHEETY_AUTH_TOKEN")
        self.headers = {
            "Authorization": self.SHEETY_AUTH_TOKEN,
            "Content-Type": "application/json",
        }

    def get_flight_prices_data(self):
        """Get flight prices data from the API.

        This method sends a GET request to the SHEETY_FLIGHTS_ENDPOINT and retrieves flight data.

        Returns:
            list: A list of flight data.
        """
        response = requests.get(url=self.SHEETY_FLIGHTS_ENDPOINT, headers=self.headers)
        response.raise_for_status()
        self.sheet_data = response.json()["prices"]
        return self.sheet_data

    def update_iata_code(self, row_id: int, iata_code: str):
        """Update the IATA code for a given row in the Google Sheet.

        This method sends a PUT request to the SHEETY_FLIGHTS_ENDPOINT to update the IATA code for a given row.

        Args:
            row_id (int): The ID of the row to update.
            iata_code (str): The IATA code to update.
        """
        update_endpoint = f"{self.SHEETY_FLIGHTS_ENDPOINT}/{row_id}"
        new_data = {
            "price": {
                "iataCode": iata_code,
            }
        }
        response = requests.put(
            url=update_endpoint, headers=self.headers, json=new_data
        )
        response.raise_for_status()
        return response.json()
