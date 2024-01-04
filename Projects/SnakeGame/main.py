from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

# Screen Setup
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)  # Turn off animations

# Object instances
snake = Snake()
food = Food()
scoreboard = Scoreboard()

# Starts listening to user key presses
screen.listen()
screen.onkey(key="Up", fun=snake.up)
screen.onkey(key="Down", fun=snake.down)
screen.onkey(key="Left", fun=snake.left)
screen.onkey(key="Right", fun=snake.right)

# Starts the game
game_is_on = True
while game_is_on:
    screen.update()  # Update the screen with new turtles drawings
    time.sleep(0.1)  # Add time delay
    snake.move()  # Move the snake forward

    # Detect collision with food.
    # If the snake's head is less than 15 pixel near a food
    if snake.head.distance(food) < 15:
        food.refresh()  # Respawn new food
        snake.grow()  # Increase the size of the snake
        scoreboard.increase_score()  # Update the scoreboard

    # Detect collision with wall.
    # If the snake's head went past the wall limits (280)
    if (
        snake.head.xcor() > 280
        or snake.head.xcor() < -280
        or snake.head.ycor() > 280
        or snake.head.ycor() < -280
    ):
        scoreboard.reset()  # Reset Game
        snake.reset()

    # Detect collision with tail
    # For each snake segments (excluding the head)
    for segment in snake.segments[1:]:
        # If the snake's head is less than 10 pixel near one of it's segment
        if snake.head.distance(segment) < 10:
            scoreboard.reset()  # Reset Game
            snake.reset()

screen.exitonclick()
