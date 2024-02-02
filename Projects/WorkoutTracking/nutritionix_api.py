import requests
from datetime import datetime


def post_workout(url, user_params, headers):
    """
    Sends a POST request to the specified URL with user parameters and headers.
    Intended to interact with an exercise tracking API like Nutritionix.

    Args:
        url (str): The API endpoint URL.
        user_params (dict): Parameters related to the user's workout session.
        headers (dict): Request headers including authentication tokens.

    Returns:
        list: A list of formatted workout data, each entry as a dictionary.
    """
    try:
        response = requests.post(url=url, json=user_params, headers=headers)
        response.raise_for_status()  # Raises an exception for 4XX/5XX responses
        data = response.json()
        return format_data(data)
    except requests.RequestException as e:
        print(f"Error while posting workout data: {e}")
        return []


def format_data(data):
    """
    Formats raw data from the exercise tracking API into a structured list.

    Args:
        data (dict): The raw data returned from the exercise tracking API.

    Returns:
        list: A list of dictionaries, each containing formatted workout data.
    """
    final_data = []
    now = datetime.now()  # Capture the current datetime once to ensure consistency
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%X")

    for exercise in data.get("exercises", []):  # Use .get to avoid KeyError
        final_data.append(
            {
                "workout": {
                    "date": date_str,
                    "time": time_str,
                    "exercise": exercise.get(
                        "name", "Unknown"
                    ).title(),  # Use .get for safer access
                    "duration": exercise.get("duration_min", 0),
                    "calories": exercise.get("nf_calories", 0),
                }
            }
        )
    return final_data
