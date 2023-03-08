from turtle import Turtle


class Snake:
    """Snake class
    """
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
        self.last_direction = self.head.heading()

    def create_snake(self):
        """Creates a Snake with 3 segments
        """
        for position in self.STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        """Adds a segment to the Snake

        Args:
            position (tuple(int, int)): the position in which assign the new segment
        """
        part = Turtle("square")
        part.color("white")
        part.penup()
        part.goto(position)
        self.segments.append(part)

    def grow(self):
        """Grows the snake by 1 segment
        """
        self.add_segment(self.segments[-1].position())

    def move(self):
        """Move the snake forward by 20 passes
        """
        for part_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[part_num - 1].xcor()
            new_y = self.segments[part_num - 1].ycor()
            self.segments[part_num].goto(new_x, new_y)
        self.head.forward(self.MOVE_DISTANCE)
        self.last_direction = self.head.heading()

    def up(self):
        """Change the heading of the snake to the north (90)
        """
        if self.head.heading() != self.DOWN and self.last_direction != self.DOWN:
            self.head.setheading(self.UP)

    def down(self):
        """Change the heading of the snake to the south (270)
        """
        if self.head.heading() != self.UP and self.last_direction != self.UP:
            self.head.setheading(self.DOWN)

    def right(self):
        """Change the heading of the snake to the east (0)
        """
        if self.head.heading() != self.LEFT and self.last_direction != self.LEFT:
            self.head.setheading(self.RIGHT)

    def left(self):
        """Change the heading of the snake to the west (180)
        """
        if self.head.heading() != self.RIGHT and self.last_direction != self.RIGHT:
            self.head.setheading(self.LEFT)
