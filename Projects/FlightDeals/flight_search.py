import os
import requests
from dotenv import load_dotenv
from pathlib import Path


class FlightSearch:
    """This class is responsible for talking to the Flight Search API."""

    def __init__(self) -> None:
        self.ENV_PATH = Path("..", "..", ".env")
        load_dotenv(dotenv_path=self.ENV_PATH)
        self.KIWI_API_KEY = os.getenv("TEQUILA_KIWI_API_KEY")
        self.KIWI_API_ENDPOINT = "https://api.tequila.kiwi.com/"
        self.headers = {
            "apikey": self.KIWI_API_KEY,
        }

    def get_iata_code(self, city: str) -> str:
        """Get the IATA code for a given city.

        This method sends a GET request to the Tequila Kiwi API to retrieve the IATA code for a given city.

        Args:
            city (str): The city to get the IATA code for.

        Returns:
            str: The IATA code for the given city.
        """
        params = {
            "term": city,
            "location_types": "city",
        }
        response = requests.get(
            url=f"{self.KIWI_API_ENDPOINT}locations/query",
            headers=self.headers,
            params=params,
        )
        response.raise_for_status()
        iata_code = response.json()["locations"][0]["code"]
        return iata_code
