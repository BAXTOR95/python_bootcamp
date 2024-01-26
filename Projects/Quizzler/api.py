import requests
import logging

API_BASE_URL = "https://opentdb.com/"

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)


def fetch_categories():
    """
    Retrieves the categories of trivia questions from the Open Trivia DB API.

    Returns:
        list[dict]: A list containing dictionaries of category information.
                    Each dictionary has 'id' and 'name' keys.
                    The first dictionary is always {"id": 0, "name": "Any Category"}.
    """
    url = f"{API_BASE_URL}api_category.php"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data_json = response.json()
        return [{"id": 0, "name": "Any Category"}] + data_json["trivia_categories"]
    except requests.RequestException as e:
        logging.error(f"Error fetching categories: {e}")
        return [{"id": 0, "name": "Any Category"}]


def fetch_trivia_questions(amount, category, difficulty):
    category_offset = 8
    category_query = 0 if category == 0 else category + category_offset
    url = f"{API_BASE_URL}api.php?amount={amount}&category={category_query}&difficulty={difficulty}&type=boolean"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching trivia questions: {e}")
        return None
