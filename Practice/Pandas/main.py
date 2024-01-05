# with open("weather_data.csv") as file:
#     data = file.readlines()
#     print(data)

# import csv

# with open("weather_data.csv") as file:
#     data = csv.reader(file)
#     temperatures = [row[1] for row in data]
#     temperatures.pop(0)
#     temperatures = [int(temperature) for temperature in temperatures]
#     print(temperatures)

import pandas as pd

# data = pd.read_csv("weather_data.csv")

# print(type(data))

# print(data["temp"])
# print(type(data["temp"]))

# data_dict = data.to_dict()
# print(data_dict)

# temp_list = data["temp"].to_list()
# print(len(temp_list))

# average_temp = data["temp"].mean()

# max_temp = data["temp"].max()

# print(average_temp)
# print(max_temp)

# # Get Data in Columns
# print(data["condition"])
# print(data.condition)

# Get Data in Row
# print(data[data.day == "Monday"])
# print(data[data.temp == data.temp.max()])

# monday = data[data.day == "Monday"]
# monday_temp = (monday.temp[0] * 9 / 5) + 32 # To Fahrenheit
# print(monday_temp)


# Create a dataframe from scratch
# data_dict = {"students": ["Amy", "James", "Brian"], "scores": [76, 56, 65]}
# df = pd.DataFrame(data_dict)
# df.to_csv("new_data.csv")

data = pd.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20240104.csv")

fur_color_count = data.groupby("Primary Fur Color").size().reset_index(name="Count")

fur_color_count.columns = ["Fur Color", "Count"]

fur_color_count.to_csv("fur_color_count.csv")
