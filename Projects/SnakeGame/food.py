from turtle import Turtle
import random


class Food(Turtle):
    """Food class
    """
    def __init__(self) -> None:
        super().__init__(shape="circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("red")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        """Respawns the food to another location
        """
        self.random_x = random.randint(-280, 280)
        self.random_y = random.randint(-280, 280)
        self.goto(self.random_x, self.random_y)
