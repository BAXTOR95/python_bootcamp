from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['name']
    password = request.form['password']
    return f'<h1>username: {username}, Password: {password}</h1>'


if __name__ == '__main__':
    app.run(debug=True)
