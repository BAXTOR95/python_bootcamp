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
            print("New lowest price found. Updating Google Sheet...")
            data_manager.update_price(row["id"], flight_data.price)
            print("Sending alert...")
            notification_manager = NotificationManager()
            message = f"Low price alert! Only ${flight_data.price} to fly from {flight_data.departure_city}-{flight_data.departure_airport_iata_code} to {flight_data.arrival_city}-{flight_data.arrival_airport_iata_code}, from {flight_data.outbound_date} to {flight_data.inbound_date}."
            if flight_data.has_stop_overs():
                message += (
                    f"\nFlight has the city of {flight_data.via_city} as layover."
                )
            notification_manager.send_sms(message=message)
            user_data = data_manager.get_user_data()
            for user in user_data:
                notification_manager.send_email(message=message, email=user["email"])
            print("Alert sent.")
