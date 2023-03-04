from turtle import Turtle, Screen
from color import get_color

# Creating the turtle object
tim = Turtle()

# Creating the screen object
screen = Screen()

# Setting the screen color-mode
screen.colormode(255)

# Drawing shapes, starting from triangle and ending in decagon
i = 3  # Sides set to 3 as starting point (triangle)
while i <= 10:  # Looping until we reach 10 sides (decagon)
    tim.pencolor(get_color())  # Change the pen color to a random color
    # Create the current shape based on the current number of sides (i)
    for _ in range(i):
        tim.forward(100)
        tim.right(360/i)
    # Return tim to starting position to begin drawing next shape
    tim.home()
    i += 1

# 'Screen object loop to prevent the window from closing without command'
screen.exitonclick()
