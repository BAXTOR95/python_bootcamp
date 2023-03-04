# https://docs.python.org/3/library/turtle.html
from turtle import Turtle, Screen

tim = Turtle()

# Draw a dashed line
# 10 passes solid line and then a gap of 10 passes (repeat 50 times)
for _ in range(50):
    if _ % 2 == 0:
        tim.pendown()
        tim.forward(10)
    else:
        tim.penup()
        tim.forward(10)


screen = Screen()
screen.exitonclick()
