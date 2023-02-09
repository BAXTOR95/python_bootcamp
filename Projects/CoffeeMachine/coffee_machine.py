class CoffeeMachine:
    """Class instance for CoffeeMachine
    """
    # instance attributes

    def __init__(self, water, milk, coffee, money):
        self.water = water
        self.milk = milk
        self.coffee = coffee
        self.money = money

# instance method
    def report(self):
        return f'Water: {self.water}ml \n' + \
            f'Milk: {self.milk}ml \n' + \
            f'Coffee: {self.coffee}g \n' + \
            f'Money: ${self.money:.2f}'

    def add_water(self, water):
        self.water += water

    def add_milk(self, milk):
        self.milk += milk

    def add_coffee(self, coffee):
        self.coffee += coffee

    def add_money(self, money):
        self.money += money

    def sub_water(self, water):
        self.water -= water

    def sub_milk(self, milk):
        self.milk -= milk

    def sub_coffee(self, coffee):
        self.coffee -= coffee

    def sub_money(self, money):
        self.money -= money
