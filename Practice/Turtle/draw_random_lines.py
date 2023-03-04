from turtle import Turtle, Screen
from color import get_color
# from random import randrange as r
from random import choice

tim = Turtle()

screen = Screen()

directions = [0, 90, 180, 270]

screen.colormode(255)

tim.width(15)
tim.speed(0)
tim.hideturtle()

for _ in range(200):
    tim.pencolor(get_color())
    tim.setheading(choice(directions))
    tim.forward(30)



# for _ in range(500):
#     direction = r(3)
#     if direction == 0:
#         tim.left(90)
#     elif direction == 1:
#         tim.right(90)
#     elif direction == 2:
#         tim.pencolor(get_color())
#         tim.forward(20)
#     else:
#         tim.pencolor(get_color())
#         tim.backward(20)

screen.exitonclick()