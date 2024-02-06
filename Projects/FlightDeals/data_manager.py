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
        response = requests.get(
            url=f"{self.SHEETY_FLIGHTS_ENDPOINT}/prices", headers=self.headers
        )
        response.raise_for_status()
        self.sheet_data = response.json()["prices"]
        return self.sheet_data

    def update_price(self, row_id: int, price: float):
        """Update the price for a given row in the Google Sheet.

        This method sends a PUT request to the SHEETY_FLIGHTS_ENDPOINT to update the price for a given row.

        Args:
            row_id (int): The ID of the row to update.
            price (int): The price to update.
        """
        update_endpoint = f"{self.SHEETY_FLIGHTS_ENDPOINT}/prices/{row_id}"
        new_data = {
            "price": {
                "lowestPrice": price,
            }
        }
        response = requests.put(
            url=update_endpoint, headers=self.headers, json=new_data
        )
        response.raise_for_status()
        return response.json()

    def update_iata_code(self, row_id: int, iata_code: str):
        """Update the IATA code for a given row in the Google Sheet.

        This method sends a PUT request to the SHEETY_FLIGHTS_ENDPOINT to update the IATA code for a given row.

        Args:
            row_id (int): The ID of the row to update.
            iata_code (str): The IATA code to update.
        """
        update_endpoint = f"{self.SHEETY_FLIGHTS_ENDPOINT}/prices/{row_id}"
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

    def get_user_data(self):
        """Get user data from the Google Sheet.

        This method sends a GET request to the SHEETY_FLIGHTS_ENDPOINT and retrieves user data.

        Returns:
            list: A list of user data.
        """
        response = requests.get(
            url=f"{self.SHEETY_FLIGHTS_ENDPOINT}/users", headers=self.headers
        )
        response.raise_for_status()
        return response.json()["users"]

    def validate_if_email_exists(self, email: str):
        """Validate if an email exists in the Google Sheet.

        This method sends a GET request to the SHEETY_FLIGHTS_ENDPOINT to validate if an email exists in the Google Sheet.

        Args:
            email (str): The email to validate.

        Returns:
            bool: True if the email exists, False otherwise.
        """
        user_data = self.get_user_data()
        for user in user_data:
            if user["email"] == email:
                return True
        return False

    def post_user_data(self, first_name: str, last_name: str, email: str):
        """Post user data to the Google Sheet.

        This method sends a POST request to the SHEETY_FLIGHTS_ENDPOINT to post user data to the Google Sheet.

        Args:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            email (str): The user's email.
        """
        new_data = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
            }
        }
        response = requests.post(
            url=f"{self.SHEETY_FLIGHTS_ENDPOINT}/users",
            headers=self.headers,
            json=new_data,
        )
        response.raise_for_status()
        return response.json()
