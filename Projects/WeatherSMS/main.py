import os
import requests
import json
from twilio.rest import Client
from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = Path('..', '..', '.env')
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"


def get_location_by_ip():
    """Retrieve the current geographic location based on IP address.

    Returns:
        tuple: A pair of float values representing latitude and longitude.
    """
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    lat, long = map(float, data['loc'].split(','))
    return lat, long


def send_sms(from_, to, body):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=from_,
        to=to,
    )

    print(message.sid)


load_dotenv(dotenv_path=ENV_PATH)

weather_app_key = os.getenv('OPEN_WEATHER_KEY')

lat, lon = get_location_by_ip()

# weather_params = {"lat": lat, "lon": lon, "appid": weather_app_key, "cnt": 4}
weather_params = {
    "lat": 29.760427,
    "lon": -95.369804,
    "appid": weather_app_key,
    "cnt": 4,
}

# response = requests.get(
#     f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_app_key}'
# )
response = requests.get(API_ENDPOINT, params=weather_params)
response.raise_for_status()

data = response.json()

weather_codes = []

for forecast in data["list"]:
    weather_data = forecast["weather"]
    for hour_data in weather_data:
        if hour_data["id"] < 700:
            weather_codes.append(hour_data["id"])

if len(weather_codes) > 0:
    twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    my_phone_number = os.getenv('MY_PHONE_NUMBER')

    send_sms(
        twilio_phone_number,
        my_phone_number,
        "It's going to rain today. Bring an umbrella!",
    )

with open("weather_data.json", mode="w") as file:
    json.dump(data, file)
