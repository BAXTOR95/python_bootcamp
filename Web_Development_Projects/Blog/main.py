import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from dotenv import load_dotenv
from notification_manager import NotificationManager
from post import Post
from config import Config

app = Flask(__name__)
load_dotenv()
app.config.from_object(Config)

if not app.config['SECRET_KEY']:
    raise ValueError("No CSRF_KEY set for Flask application")


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


def get_formatted_date():
    return datetime.now().strftime("%B %d, %Y")


@app.route('/')
def index():
    posts = Post.all_posts()

    return render_template(
        "index.html",
        posts=posts,
        header_image_url=url_for('static', filename='assets/img/home-bg.jpg'),
        date=get_formatted_date(),
    )


@app.route('/about')
def about():
    return render_template(
        'about.html',
        header_image_url=url_for('static', filename='assets/img/about-bg.jpg'),
    )


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            notification_manager = NotificationManager()
            notification_manager.send_email(form.data, app.config['MY_EMAIL'])
            flash('Thank you, your message has been sent.', 'success')
        except Exception as e:
            flash('Your message could not be sent. Please try again.', 'danger')
            app.logger.error(f"Failed to send email: {e}")
        return redirect(url_for('contact'))
    return render_template(
        'contact.html',
        form=form,  # Pass the form to the template
        header_image_url=url_for('static', filename='assets/img/contact-bg.jpg'),
    )


@app.route('/post/<int:post_id>')
def post(post_id):
    posts = Post.all_posts()
    selected_post = next((post for post in posts if post.id == post_id), None)
    if selected_post:
        return render_template(
            "post.html",
            post=selected_post,
            header_image_url=url_for('static', filename=f'assets/img/{post.image}'),
            date=get_formatted_date(),
        )
    return render_template(
        "post.html",
        post=None,
        header_image_url=url_for('static', filename='assets/img/post-bg.jpg'),
        date=get_formatted_date(),
    )


if __name__ == "__main__":
    app.run(debug=True)
