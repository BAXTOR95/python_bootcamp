import os
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('CSRF_KEY')

bootstrap = Bootstrap5(app)

if not app.config['SECRET_KEY']:
    raise ValueError("No CSRF_KEY set for Flask application")


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        label='Password', validators=[DataRequired(), Length(min=6, max=15)]
    )
    submit = SubmitField(label='Log In')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/success")
def success():
    return render_template('success.html')


@app.route("/denied")
def denied():
    return render_template('denied.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            return redirect(url_for('success'))
        else:
            return redirect(url_for('denied'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
