from turtle import Turtle

FONT = ("Courier", 8, "normal")


class StateLabel(Turtle):
    def __init__(self, state, x, y):
        super().__init__()
        self.state = state
        self.penup()
        self.hideturtle()
        self.goto(x, y)
        self.write(f"{self.state}", align="center", font=FONT)
