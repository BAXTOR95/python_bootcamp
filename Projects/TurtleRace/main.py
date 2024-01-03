from turtle import Turtle, Screen
import random

is_race_on = False
screen = Screen()
screen.setup(width=500, height=400)
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
racers = []

x = -230  # Starting X position
y = -100  # Starting Y position

# Draw the racers and position them accordingly
for _ in colors:
    racer = Turtle(shape="turtle")
    racer.color(_)
    racer.penup()
    racer.goto(x, y)
    racers.append(racer)
    y += 40  # Increase the Y position for the next racer

# Get the user bet
user_bet = screen.textinput(
    title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")

# If the user input a bet, start the race
if user_bet:
    user_bet = user_bet.lower()
    is_race_on = True

while is_race_on:

    # Move every racer randomly
    for racer in racers:
        if racer.xcor() > abs(x):  # If the racer got to the finished line first
            is_race_on = False  # End the race
            winning_color = racer.pencolor()
            if winning_color == user_bet:  # Check if winning color matches the bet
                print(f"You've won! The {winning_color} turtle is the winner!")
                break;
            else:
                print(
                    f"You've lost! The {winning_color} turtle is the winner!")
                break;

        rand_distance = random.randint(0, 10)
        racer.forward(rand_distance)  # Move the racer forward randomly


screen.exitonclick()
