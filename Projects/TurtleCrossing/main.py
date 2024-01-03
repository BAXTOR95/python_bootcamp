import time
from turtle import Screen
from player import Player, STARTING_POSITION, FINISH_LINE_Y
from car_manager import CarManager
from scoreboard import Scoreboard, FONT

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player.move_up, "Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    car_manager.create_car()
    car_manager.move_cars()

    # Detect collision with car
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            game_is_on = False
            scoreboard.goto(0, 0)
            scoreboard.write("GAME OVER", align="center", font=FONT)

    # Detect successful crossing
    if player.ycor() > FINISH_LINE_Y:
        player.goto(STARTING_POSITION)
        car_manager.level_up()
        scoreboard.increase_score()

screen.exitonclick()
