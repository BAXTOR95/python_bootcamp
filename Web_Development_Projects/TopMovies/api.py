import os
import requests
from dotenv import load_dotenv


class MovieSearch:
    """This class is responsible for talking to the Movie Search API."""

    def __init__(self) -> None:
        load_dotenv()
        self.THEMOVIEDB_API_KEY = os.getenv("THEMOVIEDB_API_KEY")
        self.THEMOVIEDB_API_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.THEMOVIEDB_API_KEY}",
        }

    def get_movie(self, movie_name: str):
        """Get the movie details for a given movie name.

        This method sends a GET request to the The Movie Database API to retrieve the details for a given movie name.

        Args:
            movie_name (str): The movie name to get the details for.

        Returns:
            dict: The movie details for the given movie name.
        """
        params = {
            "query": movie_name,
        }
        response = requests.get(
            url=self.THEMOVIEDB_API_ENDPOINT, headers=self.headers, params=params
        )
        response.raise_for_status()
        movie_details = response.json()
        return movie_details
