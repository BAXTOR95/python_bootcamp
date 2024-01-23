import requests
import time
import os
import smtplib
import pytz
from map_drawer import MapDrawer
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Your current latitude and longitude, initialized to zero
my_lat = 0
my_long = 0

# Define the path to the directory containing the .env file for environment variables
env_path = Path('..', '..', '.env')

# Load environment variables from the .env file
load_dotenv(dotenv_path=env_path)

# Access environment variables for email authentication
mail_app_pass = os.getenv('MAIL_APP_PASS')
my_email = os.getenv('MY_EMAIL')


def is_it_overhead(iss_lat, iss_long):
    """Check if the ISS is currently overhead based on latitude and longitude.

    Args:
        iss_lat (float): The latitude of the ISS.
        iss_long (float): The longitude of the ISS.

    Returns:
        bool: True if the ISS is within +/- 5 degrees of the current position, False otherwise.
    """
    return (my_lat - 5 <= iss_lat <= my_lat + 5) and (
        my_long - 5 <= iss_long <= my_long + 5
    )


def is_it_dark(sunrise, sunset, now):
    """Determine if it is currently dark at the current location.

    Args:
        sunrise (int): The hour of sunrise.
        sunset (int): The hour of sunset.
        now (int): The current hour.

    Returns:
        bool: True if current time is after sunset or before sunrise, False otherwise.
    """
    return now > sunset or now < sunrise


def get_location_by_ip():
    """Retrieve the current geographic location based on IP address.

    Returns:
        tuple: A pair of float values representing latitude and longitude.
    """
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    lat, long = map(float, data['loc'].split(','))
    return lat, long


def get_iss_location():
    """Fetch the current location of the International Space Station (ISS).

    Returns:
        tuple: Latitude and longitude of the ISS.
    """
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return iss_latitude, iss_longitude


def set_current_lat_long():
    """Sets current latitude and longitude globally"""
    global my_lat, my_long
    my_lat, my_long = get_location_by_ip()


def get_sunrise_sunset():
    """Retrieve sunrise and sunset times for the current location.

    Returns:
        tuple: Sunrise and sunset hours.
    """
    parameters = {"lat": my_lat, "lng": my_long, "formatted": 0}
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    return sunrise, sunset


def main():
    """Main function to track the ISS and send an email notification."""
    iss_latitude, iss_longitude = get_iss_location()
    set_current_lat_long()
    sunrise, sunset = get_sunrise_sunset()
    tz = pytz.timezone('EST')
    time_now = datetime.now(tz)

    # Update to provide more information
    print(f"ISS Current Location: Lat {iss_latitude}, Long {iss_longitude}")
    print(f"My Location: Lat {my_lat}, Long {my_long}")

    if is_it_overhead(iss_latitude, iss_longitude):
        print("The ISS is close to your location!")
    else:
        print("The ISS is not close enough...")

    if is_it_dark(sunrise, sunset, time_now.hour):
        print("It's dark enough to spot the ISS.")
    else:
        print("It's not dark yet.")

    map_drawer = MapDrawer((my_lat, my_long))
    iss_map = map_drawer.prepare_map((iss_latitude, iss_longitude))
    print(iss_map)

    if is_it_overhead(iss_latitude, iss_longitude) and is_it_dark(
        sunrise, sunset, time_now.hour
    ):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=mail_app_pass)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg="Subject: Look Up!\n\nThe ISS is above you!",
            )
            print("Email sent!")
    else:
        print("ISS is not above current location...")


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)
