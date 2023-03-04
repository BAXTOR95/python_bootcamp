from turtle import Turtle, Screen
from color import get_color

tim = Turtle()
screen = Screen()

screen.colormode(255)

tim.speed(0)


def draw_spirograph(size_of_gap):
    for _ in range(int(360 / size_of_gap)):
        tim.color(get_color())
        tim.circle(100)
        tim.setheading(tim.heading() + size_of_gap)

draw_spirograph(10)

screen.exitonclick()
