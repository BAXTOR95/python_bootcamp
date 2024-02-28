import random
import requests

from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    random_number = random.randint(1, 3)
    year = datetime.now().year
    return render_template('index.html', num=random_number, year=year)


def request_gender_api(name):
    response = requests.get(f'https://api.genderize.io?name={name}')
    response.raise_for_status()
    data = response.json()

    return data["gender"]


def request_age_api(name):
    response = requests.get(f'https://api.agify.io?name={name}')
    response.raise_for_status()
    data = response.json()

    return data["age"]


@app.route('/guess/<name>')
def guess(name):
    gender = request_gender_api(name)
    age = request_age_api(name)
    return render_template('guess.html', name=name, age=age, gender=gender)


@app.route('/blog/<int:num>')
def get_blog(num):
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts, num=num)


if __name__ == '__main__':
    app.run(debug=True)
