from turtle import Turtle


class Paddle(Turtle):
    """Paddle class
    """
    MOVE_DISTANCE = 20
    NORTH = 90
    Y_LIMIT = 220

    def __init__(self, x_pos, y_pos) -> None:
        super().__init__("square")
        self.color("white")
        self.resizemode("user")
        self.shapesize(1, 5, 0)
        self.setheading(self.NORTH)
        self.penup()
        self.goto((x_pos, y_pos))

    def move_up(self):
        """Moves the paddle up
        """
        if self.ycor() < self.Y_LIMIT:
            self.forward(self.MOVE_DISTANCE)

    def move_down(self):
        """Moves the paddle down
        """
        if self.ycor() > -self.Y_LIMIT:
            self.backward(self.MOVE_DISTANCE)
