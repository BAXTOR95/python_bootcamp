from __future__ import annotations
from typing import List
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Integer, String, Text, ForeignKey
from flask_ckeditor import CKEditor
from datetime import date
from notification_manager import NotificationManager
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)
from hashlib import md5
from config import Config

# Import commands
from commands import create_admin

# Import forms from the forms.py
from forms import BlogPostForm, ContactForm, RegisterForm, LoginForm, CommentForm

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config.from_object(Config)
Bootstrap5(app)

# Register the command
app.cli.add_command(create_admin)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# Setup Gravatar
def gravatar_url(email, size=100, rating='g', default='retro', force_default=False):
    hash_value = md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_value}?s={size}&d={default}&r={rating}&f={force_default}"


# User Loader
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


share_data = {'year': date.today().year}


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    is_admin: Mapped[bool] = mapped_column(Integer, default=0)

    # *******Add parent relationship*******#
    # This will act like a List of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts: Mapped[List["BlogPost"]] = relationship("BlogPost", back_populates="author")
    # "comment_author" refers to the comment_author property in the Comment class.
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="comment_author"
    )


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # *******Add parent relationship*******#
    comments = relationship("Comment", back_populates="parent_post")

    # *******Add child relationship*******#
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    # Create reference to the User object. The "posts" refers to the posts property in the User class.
    author: Mapped["User"] = relationship("User", back_populates="posts")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    # *******Add child relationship*******#
    # "users.id" The users refers to the tablename of the Users class.
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    # "comments" refers to the comments property in the User class.
    comment_author: Mapped["User"] = relationship("User", back_populates="comments")
    # "blog_post.id" The blog_post refers to the tablename of the BlogPost class.
    post_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    # "comments" refers to the comments property in the BlogPost class.
    parent_post: Mapped["BlogPost"] = relationship(
        "BlogPost", back_populates="comments"
    )


with app.app_context():
    db.create_all()


def get_all_posts():
    stmt = db.select(BlogPost).order_by(BlogPost.date.desc())
    return db.session.execute(stmt).scalars().all()


def get_post(post_id):
    stmt = db.select(BlogPost).where(BlogPost.id == post_id)
    return db.session.execute(stmt).scalar()


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("You must be an admin to view this page.", "warning")
            return redirect(url_for('index'))
        return f(*args, **kwargs)

    return decorated_function

def only_commenter(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = db.session.execute(db.select(Comment).where(Comment.author_id == current_user.id)).scalar()
        if not current_user.is_authenticated or current_user.id != user.author_id:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


if not app.config['SECRET_KEY']:
    raise ValueError("No CSRF_KEY set for Flask application")


@app.context_processor
def inject_data():
    return {'share_data': share_data}


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            name = form.name.data
            password = form.password.data
            password2 = form.password2.data
            if password != password2:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('register'))
            hashed_password = generate_password_hash(
                password, method='pbkdf2:sha256', salt_length=8
            )
            new_user = User(email=email, name=name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            flash("That email already exists, please login.", category='error')
            return redirect(url_for('login'))
    return render_template(
        "register.html",
        form=form,
        header_image_url=url_for('static', filename='assets/img/register.jpg'),
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid email or password.', 'danger')
    return render_template(
        "login.html",
        form=form,
        header_image_url=url_for('static', filename='assets/img/login.jpg'),
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", category='success')
    return redirect(url_for('index'))


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


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = get_post(post_id)
    if post:
        form = CommentForm()
        if form.validate_on_submit() and current_user.is_authenticated:
            new_comment = Comment(
                text=form.comment.data,
                author_id=current_user.id,
                comment_author=current_user,
                post_id=post_id,
                parent_post=post,
            )
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added!', 'success')
            return redirect(url_for('post', post_id=post_id))
        return render_template(
            "post.html",
            post=post,
            form=form,
            gravatar_url=gravatar_url,
            header_image_url=post.img_url,
        )
    return render_template(
        "post.html",
        post=None,
        form=form,
        gravatar_url=gravatar_url,
        header_image_url=url_for('static', filename='assets/img/post-bg.jpg'),
    )


@app.route('/new-post', methods=['GET', 'POST'])
@login_required
@admin_required
def new_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            img_url=form.img_url.data,
            author_id=current_user.id,
            author=current_user,
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
@login_required
@admin_required
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
@login_required
@admin_required
def delete_post(post_id):
    post = db.session.get(BlogPost, post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', 'success')
    return redirect(url_for('index'))

@app.route("/delete/comment/<int:comment_id>/<int:post_id>")
@only_commenter
def delete_comment(post_id, comment_id):
    post_to_delete = db.get_or_404(Comment, comment_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))

if __name__ == "__main__":
    app.run(debug=True, port=5002)
