import os
import json
from dotenv import load_dotenv
from pathlib import Path
from nutritionix_api import post_workout
from sheety_api import add_to_spreadsheet

# Constants
ENV_PATH = Path("..", "..", ".env")
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
USER_DATA_PATH = os.path.join(CURRENT_DIRECTORY, "user_data.json")

# Load environment variables
load_dotenv(dotenv_path=ENV_PATH)

# Nutritionix API Configuration
NUTRITIONIX_APP_KEY = os.getenv("NUTRITIONIX_APP_KEY")
NUTRITIONIX_APP_ID_KEY = os.getenv("NUTRITIONIX_APP_ID_KEY")
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

# Sheety API Configuration
SHEETY_AUTH_TOKEN = os.getenv("SHEETY_AUTH_TOKEN")
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")


def validate_number(input_value, expected_type='float'):
    """
    Validates if the given input_value is of the specified expected_type.

    Args:
        input_value (str): The value to validate.
        expected_type (str): The type to validate against ('float' or 'int').

    Returns:
        tuple: (bool indicating validity, converted value or 'invalid')
    """
    try:
        float_val = float(input_value)
        if expected_type == 'int' and float_val.is_integer():
            return True, int(float_val)
        elif expected_type == 'float':
            return True, float_val
    except ValueError:
        pass

    return False, 'invalid'


def get_user_input(prompt, expected_type='float'):
    """
    Continuously prompts the user for input until a valid number is entered.

    Args:
        prompt (str): The prompt to display to the user.
        expected_type (str): The expected numerical type ('float' or 'int').

    Returns:
        float or int: The validated user input.
    """
    while True:
        user_input = input(prompt)
        is_valid, value = validate_number(user_input, expected_type)
        if is_valid:
            return value
        print(f"Invalid {expected_type}. Please enter a valid number.")


def get_user_data():
    """
    Retrieves user data from a JSON file or prompts the user to enter their data.

    Returns:
        dict: A dictionary containing the user's weight, height, and age.
    """
    try:
        with open(USER_DATA_PATH, 'r') as file:
            # Use verify_user_data to check if the data is valid before returning
            user_data = json.load(file)
            if verify_user_data(user_data):
                return user_data
            else:
                raise json.JSONDecodeError
    except (FileNotFoundError, json.JSONDecodeError):
        weight_kg = get_user_input("What's your weight in kg? ", 'float')
        height_cm = get_user_input("What's your height in cm? ", 'float')
        age = get_user_input("What's your age? ", 'int')

        data = {"weight_kg": weight_kg, "height_cm": height_cm, "age": age}

        with open(USER_DATA_PATH, mode="w") as file:
            json.dump(data, file, indent=4)

        return data


def verify_user_data(user_data):
    """
    Verifies that the user data is valid.

    Args:
        user_data (dict): The user's weight, height, and age.

    Returns:
        bool: True if the user data is valid, False otherwise.
    """
    if not all(key in user_data for key in ("weight_kg", "height_cm", "age")):
        return False

    if not all(isinstance(value, (int, float)) for value in user_data.values()):
        return False

    return True


# Main Execution
if __name__ == "__main__":
    # Nutritionix API request
    user_data = get_user_data()
    user_params = {
        "query": input("Tell me which exercises you did: "),
        "weight_kg": user_data["weight_kg"],
        "height_cm": user_data["height_cm"],
        "age": user_data["age"],
    }

    nutritionix_headers = {
        "x-app-id": NUTRITIONIX_APP_ID_KEY,
        "x-app-key": NUTRITIONIX_APP_KEY,
        "x-remote-user-id": "0",
    }

    exercise_data = post_workout(NUTRITIONIX_ENDPOINT, user_params, nutritionix_headers)

    # Sheety API request
    sheety_headers = {
        "Authorization": SHEETY_AUTH_TOKEN,
        'Content-Type': 'application/json',
    }
    for exercise in exercise_data:
        add_to_spreadsheet(SHEETY_ENDPOINT, exercise, sheety_headers)
