from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

# Screen setup
screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong Game")
screen.tracer(0)

# Object instances
p1 = Paddle(-350, 0)
p2 = Paddle(350, 0)
ball = Ball()
scoreboard = Scoreboard()

# Starts listening to user key presses
screen.listen()
screen.onkeypress(p1.move_up, "w")
screen.onkeypress(p1.move_down, "s")
screen.onkeypress(p2.move_up, "Up")
screen.onkeypress(p2.move_down, "Down")

# Starts the game
game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Detect collision with wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.wall_bounce()

    # Detect collision with right paddle
    if ball.distance(p2) < 50 and ball.xcor() > 320:
        ball.paddle_2_bounce()

    # Detect collision with right paddle
    if ball.distance(p1) < 50 and ball.xcor() < -320:
        ball.paddle_1_bounce()

    # Detect collision with p1 wall
    if ball.xcor() < -380:
        scoreboard.p1_point()
        ball.refresh()

    # Detect collision with p2 wall
    if ball.xcor() > 380:
        scoreboard.p2_point()
        ball.refresh()

screen.exitonclick()
