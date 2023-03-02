class Coin:
    """Class instance for coin (can be any coin. E.g. quarter, dime, nickle
        penny, etc.)
    """

    def __init__(self, value: float):
        self.__value = value
        self.__count: int = 0

    def value(self):
        return self.__value

    def count(self):
        return self.__count

    def set_count(self, quantity: int):
        self.__count = quantity

    def total_value(self):
        return self.__value * self.__count
