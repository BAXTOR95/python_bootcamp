import requests


def add_to_spreadsheet(url, data, headers):
    """
    Sends a POST request to add a new row of data to a spreadsheet via an API, such as Sheety.

    Args:
        url (str): The API endpoint URL for adding data to the spreadsheet.
        data (dict): The data to be added to the spreadsheet, formatted as per the API requirements.
        headers (dict): Headers for the request, typically including authorization and content type.

    Returns:
        bool: True if the data was added successfully, False otherwise.

    Prints the API response data to the console for logging and debugging purposes.
    """
    try:
        response = requests.post(url=url, json=data, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4XX, 5XX)

        # Print and return success status
        response_data = response.json()
        print("Data successfully added to the spreadsheet:", response_data)
        return True
    except requests.RequestException as e:
        # Handle and print all possible request exceptions, including HTTPError, ConnectionError, etc.
        print(f"Failed to add data to the spreadsheet. Error: {e}")
        return False
