from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()


def move_forward():
    """Move turtle forward by 10 paces
    """
    tim.forward(10)


def move_backward():
    """Move turtle backwards by 10 paces
    """
    tim.backward(10)


def rotate_counter_clockwise():
    """Rotate turtle counter clockwise
    """
    current_heading = tim.heading()
    tim.setheading(current_heading+10)


def rotate_clockwise():
    """Rotate turtle clockwise
    """
    current_heading = tim.heading()
    tim.setheading(current_heading-10)


screen.listen()  # Starts listening for key presses
screen.onkey(fun=move_forward, key="w")
screen.onkey(fun=move_backward, key="s")
screen.onkey(fun=rotate_counter_clockwise, key="a")
screen.onkey(fun=rotate_clockwise, key="d")
screen.onkey(fun=screen.reset, key="c")
screen.exitonclick()
