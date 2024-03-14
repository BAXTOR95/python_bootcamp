import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, URL
from dotenv import load_dotenv
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from notification_manager import NotificationManager
from config import Config

app = Flask(__name__)
ckeditor = CKEditor(app)
load_dotenv()
app.config.from_object(Config)
Bootstrap5(app)

share_data = {'year': date.today().year}


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


def get_all_posts():
    stmt = db.select(BlogPost).order_by(BlogPost.date.desc())
    return db.session.execute(stmt).scalars().all()


def get_post(post_id):
    stmt = db.select(BlogPost).where(BlogPost.id == post_id)
    return db.session.execute(stmt).scalar()


if not app.config['SECRET_KEY']:
    raise ValueError("No CSRF_KEY set for Flask application")

####### FORMS #######


# CONTACT FORM
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


# BLOG POST FORM
class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit Post')


@app.context_processor
def inject_share_data():
    return {'share_data': share_data}


@app.route('/')
def index():
    posts = get_all_posts()

    return render_template(
        "index.html",
        posts=posts,
        header_image_url=url_for('static', filename='assets/img/home-bg.jpg'),
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
    post = get_post(post_id)
    if post:
        return render_template("post.html", post=post, header_image_url=post.img_url)
    return render_template(
        "post.html",
        post=None,
        header_image_url=url_for('static', filename='assets/img/post-bg.jpg'),
    )


@app.route('/new-post', methods=['GET', 'POST'])
def new_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data,
            date=datetime.now().strftime('%B %d, %Y'),
        )
        db.session.add(new_post)
        db.session.commit()
        flash('New post added!', 'success')
        return redirect(url_for('index'))
    return render_template(
        'make-post.html',
        form=form,
        act="new_post",
        header_image_url=url_for('static', filename='assets/img/post-bg.jpg'),
    )


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.session.get(BlogPost, post_id)
    if post:
        form = BlogPostForm(
            title=post.title,
            subtitle=post.subtitle,
            author=post.author,
            img_url=post.img_url,
            body=post.body,
        )
        if form.validate_on_submit():
            post.title = form.title.data
            post.subtitle = form.subtitle.data
            post.author = form.author.data
            post.img_url = form.img_url.data
            post.body = form.body.data
            db.session.commit()
            flash('Post updated!', 'success')
            return redirect(url_for('post', post_id=post_id))
        return render_template(
            'make-post.html',
            form=form,
            act="edit_post",
            post_id=post_id,
            header_image_url=post.img_url,
        )
    return redirect(url_for('index'))


@app.route('/delete-post/<int:post_id>')
def delete_post(post_id):
    post = db.session.get(BlogPost, post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', 'success')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
