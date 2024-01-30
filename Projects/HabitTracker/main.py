import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

ENV_PATH = Path("..", "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)

pixela_endpoint = "https://pixe.la/v1/users"
TOKEN = os.getenv("PIXELA_TOKEN")
USERNAME = os.getenv("PIXELA_USERNAME")
GRAPH_ID = "graph1"


user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

## User Creation
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

## Graph Definition
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": GRAPH_ID,
    "name": "Gym Graph",
    "unit": "hrs",
    "type": "float",
    "color": "sora",
}

headers = {"X-USER-TOKEN": TOKEN}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

## Post value to the graph
graph_update_endpoint = f"{graph_endpoint}/{GRAPH_ID}"
date = datetime(year=2024, month=1, day=26)
quantity = "1"
data = {"date": date.strftime("%Y%m%d"), "quantity": quantity}

response = requests.post(url=graph_update_endpoint, json=data, headers=headers)
print(response.text)

# response = requests.put(url=graph_update_endpoint, json=graph_config, headers=headers)
# print(response.text)
