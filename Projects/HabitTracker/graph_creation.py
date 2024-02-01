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
GRAPH_ID = "graph1"
headers = {"X-USER-TOKEN": TOKEN}
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

## Graph Definition
graph_config = {
    "id": GRAPH_ID,
    "name": "Gym Graph",
    "unit": "hrs",
    "type": "float",
    "color": "sora",
}

response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
print(response.text)
