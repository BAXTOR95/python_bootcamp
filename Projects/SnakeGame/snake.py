from turtle import Turtle


class Snake:

    STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
    MOVE_DISTANCE = 20
    UP = 90
    DOWN = 270
    RIGHT = 0
    LEFT = 180

    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for position in self.STARTING_POSITIONS:
            part = Turtle("square")
            part.color("white")
            part.penup()
            part.goto(position)
            self.segments.append(part)

    def move(self):
        for part_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[part_num - 1].xcor()
            new_y = self.segments[part_num - 1].ycor()
            self.segments[part_num].goto(new_x, new_y)
        self.head.forward(self.MOVE_DISTANCE)

    def up(self):
        current_heading = self.head.heading()
        if current_heading != self.UP and current_heading != self.DOWN:
            self.head.setheading(self.UP)

    def down(self):
        current_heading = self.head.heading()
        if current_heading != self.UP and current_heading != self.DOWN:
            self.head.setheading(self.DOWN)

    def right(self):
        current_heading = self.head.heading()
        if current_heading != self.RIGHT and current_heading != self.LEFT:
            self.head.setheading(self.RIGHT)

    def left(self):
        current_heading = self.head.heading()
        if current_heading != self.RIGHT and current_heading != self.LEFT:
            self.head.setheading(self.LEFT)
