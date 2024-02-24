from flask import Flask
from random import randint
from functools import wraps

app = Flask(__name__)

number_to_guess = randint(0, 9)


def make_div(function):
    @wraps(function)
    def wrapper_function(*args, **kwargs):
        return f"<div>{function(*args, **kwargs)}</div>"

    return wrapper_function


@app.route("/")
@make_div
def home_page():
    return """
            <h1>Guess a number between 0 and 9</h1>
            <img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" alt="Numbers from 0 to 9">
            """


@app.route("/<int:guess>")
@make_div
def guess_number(guess):
    if guess == number_to_guess:
        return (
            f"<h1 style='color: green'>You found me! The number is {number_to_guess}</h1>"
            "<img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHJ1cTVyZnZzdW1yOXNlNnQzY2dldmt5a3FsODhjZjFod3diZGU0dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YTbZzCkRQCEJa/giphy.gif' alt='You found me!'>"
        )
    elif guess < number_to_guess:
        return (
            f"<h1 style='color: red'>Too low, try again!</h1>"
            "<img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnE0OWdoYTB4a3h4emZ1cXRocW0zNHB6NWdkNnB6NG1scWlrYmUxMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ISOckXUybVfQ4/giphy.gif' alt='Too low!'>"
        )
    else:
        return (
            f"<h1 style='color: purple'>Too high, try again!</h1>"
            "<img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG5hMW9iMmp5cTJtYnFka3l1eG5qMmNyODNyYW9jZnJlc3JwMWRqMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yoJC2Olx0ekMy2nX7W/giphy.gif' alt='Too high!'>"
        )


if __name__ == "__main__":
    app.run(debug=True)
