# https://docs.python.org/3/library/turtle.html
from turtle import Turtle, Screen

tim = Turtle()
tim.shape("turtle")
tim.color("cyan")

# Draw a square
for _ in range(4):
    tim.forward(100)
    tim.right(90)


screen = Screen()
screen.exitonclick()
