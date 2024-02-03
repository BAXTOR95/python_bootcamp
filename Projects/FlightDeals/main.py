# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

# from pprint import pprint

data_manager = DataManager()
sheet_data = data_manager.get_flight_prices_data()
# pprint(sheet_data)

# Check if sheet_data has empty IATA codes
flight_search = FlightSearch()

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_iata_code(row["city"])
        data_manager.update_iata_code(row["id"], row["iataCode"])

# print("Updated sheet data:\n")
# pprint(sheet_data)

for row in sheet_data:
    flight_data = FlightData()
    print(f"Checking for flights to {row['city']} - {row['iataCode']}.")
    flight_data.get_flight_prices(row["iataCode"])
    if flight_data.has_flight_data():
        print("Flight data available.")
        print(
            f"Comparing found price ({flight_data.price}) vs lowest price previously known ({row['lowestPrice']})"
        )
        if flight_data.price < row["lowestPrice"]:
            print("New lowest price found. Sending alert...")
            notification_manager = NotificationManager()
            notification_manager.send_sms(
                message=f"Low price alert! Only ${flight_data.price} to fly from {flight_data.departure_city}-{flight_data.departure_airport_iata_code} to {flight_data.arrival_city}-{flight_data.arrival_airport_iata_code}, from {flight_data.outbound_date} to {flight_data.inbound_date}."
            )
            print("Alert sent.")
