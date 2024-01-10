# def add(*args):
#     x = 0
#     for a in args:
#         x += a
#     return x


# def add(*args):
#     return sum(args)


# # Ask the user for input
# user_input = input("Enter numbers separated by spaces: ")

# # Split the input string into a list and convert each item to an integer or float
# numbers = [float(num) for num in user_input.split()]

# # Call the add function with the unpacked list of numbers
# result = add(*numbers)

# print("The sum is:", result)


# def calculate(n, **kwargs):
#     n += kwargs["add"]
#     n *= kwargs["multiply"]
#     print(n)


# calculate(2, add=3, multiply=5)


class Car:
    def __init__(self, *args, **kwargs):
        self.make = kwargs.get("make")
        self.model = kwargs.get("model")
        self.color = kwargs.get("color")
        self.seats = kwargs.get("seats")


my_car = Car(make="Nissan", model="GT-R")
print(my_car.model)
