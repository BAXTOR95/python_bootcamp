import requests
from datetime import datetime

MY_LAT = 28.538336
MY_LONG = -81.379234

# response = requests.get(url="http://api.open-notify.org/iss-now.json")
# response.raise_for_status()

# data = response.json()
# longitude = data["iss_position"]["longitude"]
# latitude = data["iss_position"]["latitude"]
# iss_position = (longitude, latitude)

# print(iss_position)

# parameters = {"lat": MY_LAT, "lng": MY_LONG, "formatted": 0}

# response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
# response.raise_for_status()
# data = response.json()
# sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
# sunset = data["results"]["sunset"].split("T")[1].split(":")[0]

# time_now = datetime.now()

# print(f"Sunrise Hour: {sunrise}\nSunset Hour: {sunset}\nCurrent Time: {time_now.hour}")


def get_location_by_ip():
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    lat, long = map(float, data['loc'].split(','))
    return lat, long


my_lat, my_long = get_location_by_ip()
print("Latitude:", my_lat, "Longitude:", my_long)
