class CoffeeMachine:
    """Class instance for CoffeeMachine
    """
    # instance attributes

    def __init__(self, water: float, milk: float, coffee: float, money: float):
        self.__water = water
        self.__milk = milk
        self.__coffee = coffee
        self.__money = money

# instance method
    def report(self) -> str:
        return f'Water: {self.__water}ml \n' + \
            f'Milk: {self.__milk}ml \n' + \
            f'Coffee: {self.__coffee}g \n' + \
            f'Money: ${self.__money:.2f}'

    def water(self):
        return self.__water

    def milk(self):
        return self.__milk

    def coffee(self):
        return self.__coffee

    def money(self):
        return self.__money

    def add_water(self, water: float):
        self.__water += water

    def add_milk(self, milk: float):
        self.__milk += milk

    def add_coffee(self, coffee: float):
        self.__coffee += coffee

    def add_money(self, money: float):
        self.__money += money

    def sub_water(self, water: float):
        self.__water -= water

    def sub_milk(self, milk: float):
        self.__milk -= milk

    def sub_coffee(self, coffee: float):
        self.__coffee -= coffee

    def sub_money(self, money: float):
        self.__money -= money
