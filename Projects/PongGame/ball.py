from turtle import Turtle


class Ball(Turtle):
    """Ball class
    """
    X_INCREMENT = 10
    Y_INCREMENT = 10
    MOVE_SPEED = 0.1

    def __init__(self) -> None:
        super().__init__("circle")
        self.color("white")
        self.penup()
        self.x_increment = self.X_INCREMENT
        self.y_increment = self.Y_INCREMENT
        self.move_speed = self.MOVE_SPEED

    def move(self):
        """Moves the ball
        """
        new_x = self.xcor() + self.x_increment
        new_y = self.ycor() + self.y_increment
        self.goto(new_x, new_y)

    def refresh(self):
        """Resets the ball and it's speed
        """
        self.home()
        self.move_speed = self.MOVE_SPEED
        self.x_increment *= -1

    def wall_bounce(self):
        """Bounces the ball off the wall
        """
        self.y_increment *= -1

    def paddle_1_bounce(self):
        """Bounces the ball off the paddle 1
        """
        self.x_increment = abs(self.x_increment)
        self.move_speed *= 0.9

    def paddle_2_bounce(self):
        """Bounces the ball off the paddle 2
        """
        self.x_increment = -(abs(self.x_increment))
        self.move_speed *= 0.9
