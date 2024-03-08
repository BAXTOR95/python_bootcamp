import os
import requests

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL
from dotenv import load_dotenv
from api import MovieSearch

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('CSRF_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Search')


class EditMovieForm(FlaskForm):
    rating = FloatField('Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')


def add_movie(title, year, description, rating, review, img_url):
    with app.app_context():
        new_movie = Movie(
            title=title,
            year=year,
            description=description,
            rating=rating,
            review=review,
            img_url=img_url,
        )
        db.session.add(new_movie)
        db.session.commit()
        return new_movie.id


def get_movies():
    with app.app_context():
        stmt = db.select(Movie).order_by(Movie.rating.desc())
        results = db.session.execute(stmt).scalars().all()
        # Enumerate over results, starting the index at 1 for ranking
        ranked_movies = [(rank, movie) for rank, movie in enumerate(results, start=1)]
        # Reverse the list to have ranks in ascending order
        ranked_movies = ranked_movies[::-1]
        return ranked_movies


def get_movie(movie_id):
    with app.app_context():
        stmt = db.select(Movie).where(Movie.id == movie_id)
        result = db.session.execute(stmt)
        return result.scalars().first()


def update_movie(movie_id, rating, review):
    with app.app_context():
        movie = db.session.get(Movie, movie_id)
        if movie:
            movie.rating = rating
            movie.review = review
            db.session.commit()


@app.route("/")
def home():
    return render_template("index.html", movies=get_movies())


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = MovieForm()
    if form.validate_on_submit():
        movies_search = MovieSearch()
        movies_data = movies_search.get_movie(form.title.data)

        if movies_data['results']:
            return render_template("select.html", movies_data=movies_data['results'])
        else:
            flash('No movie found with this title. Please try again.', 'danger')
    return render_template("add.html", form=form)

@app.route("/select-movie")
def select_movie():
    try:
        movie_id = add_movie(
            title=request.args.get('title'),
            year=request.args.get('year'),
            description=request.args.get('description'),
            rating=0,
            review='',
            img_url=f"https://image.tmdb.org/t/p/w500{request.args.get('img_url')}",
        )
        return redirect(url_for('edit', movie_id=movie_id))
    except IntegrityError:
        db.session.rollback()  # Roll back the session to a clean state
        flash(
            'A movie with this title already exists. Please use a different title.',
            'danger',
        )


@app.route('/edit-movie/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    form = EditMovieForm()
    if form.validate_on_submit():
        update_movie(movie_id, form.rating.data, form.review.data)
        return redirect(url_for('home'))
    return render_template('edit.html', form=form, movie=get_movie(movie_id))


@app.route('/delete/<int:movie_id>', methods=['GET', 'POST'])
def delete(movie_id):
    with app.app_context():
        movie_to_delete = db.session.get(Movie, movie_id)
        if movie_to_delete:
            db.session.delete(movie_to_delete)
            db.session.commit()
        return redirect(url_for('home'))


if __name__ == '__main__':
    # Create table
    with app.app_context():
        db.create_all()

    app.run(debug=True)
