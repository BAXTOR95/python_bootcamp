import turtle as t
import random

# import colorgram

# e_colors = colorgram.extract('painting.jpg',30)

# colors = []

# for color in e_colors:
#     colors.append((color.rgb.r, color.rgb.g, color.rgb.b))

# print(colors)

background_color = (246, 243, 239)  # Color for the background

# Colors picked from hirst painting
colors = [(202, 166, 109), (152, 73, 47), (170, 153, 41), (222, 202, 138),
          (53, 93, 124), (135, 32, 22), (132, 163, 184), (48, 118, 88),
          (198, 91, 71), (16, 97, 75), (100, 73, 75), (67, 47, 41),
          (147, 178, 147), (163, 142, 156), (234, 177, 165), (55, 46, 50),
          (130, 28, 31), (184, 205, 174), (41, 60, 72), (83, 147, 126),
          (181, 87, 90), (31, 77, 84), (47, 65, 83), (215, 177, 182),
          (19, 71, 63), (175, 192, 212)]

# Creating the turtle object
hirst = t.Turtle()

# Hiding the turtle
hirst.hideturtle()

# Speeding the turtle
hirst.speed(0)

# Creating the screen object
screen = t.Screen()

# Setting the screen color-mode
screen.colormode(255)

# Setting the background color
screen.bgcolor(background_color)


def draw_painting(grid_size=(10, 10), space=50, dot_size=20):
    """Draws a Hirst Spot painting giving the grid size and space between dots

    Args:
        grid_size (tuple, optional): the size of the grid as (x,y). Defaults to (10,10).
        space (int, optional): space between the dots. Defaults to 50.
        dot_size (int, optional): size of dots. Defaults to 20.
    """
    x = grid_size[0]  # Extracts X
    y = grid_size[1]  # Extracts Y
    pos_x = -(x*space)/2  # Starting position for X axis
    pos_y = -(y*space)/2  # Starting position for Y axis
    # Setting screen size to match grid size
    screen.screensize(x*space, y*space)
    hirst.penup()  # Hides the pen
    # Set starting positions to make the painting centered
    hirst.setpos((pos_x, pos_y))
    for y_row in range(y):  # Y axis loop
        for x_row in range(x):  # X axis loop
            hirst.dot(dot_size, random.choice(colors))
            if x_row < x - 1:  # If we are not at the last dot, keep moving forward
                hirst.forward(space)
        hirst.setx(pos_x)  # Go back to starting position
        hirst.sety(hirst.position()[1] + space)  # Move up to the next row


# Draw the painting
draw_painting()

# Exit on mouse click
screen.exitonclick()
