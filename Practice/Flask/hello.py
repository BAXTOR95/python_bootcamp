from flask import Flask
from markupsafe import escape

app = Flask(__name__)


def make_div(function):
    def wrapper_function():
        return f"<div>{function()}</div>"

    return wrapper_function


def make_paragraph(function):
    def wrapper_function():
        return f"<p>{function()}</p>"

    return wrapper_function


def make_bold(function):
    def wrapper_function():
        return f"<b>{function()}</b>"

    return wrapper_function


def make_emphasis(function):
    def wrapper_function():
        return f"<i>{function()}</i>"

    return wrapper_function


def make_underline(function):
    def wrapper_function():
        return f"<u>{function()}</u>"

    return wrapper_function


@app.route("/")
@make_div
def hello_world():
    return """
        <h1 style="text-align: center">Hello, World!</h1>
        <p>This is a paragraph</p>
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3pqYjd3anFwM3A2ZGl4ZGp2ZXh0c2Z1NDd5dGU3dHhyYXdvMjU4NyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/StKiS6x698JAl9d6cx/giphy.gif" alt="minion dancing">
        """


@app.route("/bye")
@make_paragraph
@make_bold
@make_emphasis
@make_underline
def say_bye():
    return "Bye!"


@app.route("/greet/<name>/<int:number>")
@make_paragraph
def greet(name, number):
    return f"Hello, {escape(name.capitalize())}! You are {number} years old!"


if __name__ == "__main__":
    # Run the app in debug mode to auto-reload the server
    app.run(debug=True)
