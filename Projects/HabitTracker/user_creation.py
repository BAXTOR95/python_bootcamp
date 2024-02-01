import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ENV_PATH = Path("..", "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)

# Pixela details
pixela_endpoint = "https://pixe.la/v1/users"
TOKEN = os.getenv("PIXELA_TOKEN")
USERNAME = os.getenv("PIXELA_USERNAME")

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

## User Creation
response = requests.post(url=pixela_endpoint, json=user_params)
print(response.text)
