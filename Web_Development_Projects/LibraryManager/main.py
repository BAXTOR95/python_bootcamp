import os

from flask import Flask, redirect, render_template, flash, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Integer, String, Float
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('CSRF_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
Bootstrap5(app)

RATING_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
]


# Create the database
class Base(DeclarativeBase):
    pass


# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)


class Books(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<Books {self.title}>'


class BookForm(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired()])
    book_author = StringField('Book Author', validators=[DataRequired()])
    book_rating = SelectField(
        'Rating',
        choices=RATING_CHOICES,
        validators=[DataRequired()],
    )
    submit = SubmitField('Submit')


# Define the form for editing a book rating
class EditRatingForm(FlaskForm):
    rating = SelectField(
        'Rating',
        choices=RATING_CHOICES,
        validators=[DataRequired()],
    )
    submit = SubmitField('Change Rating')


def get_all_books():
    with app.app_context():
        stmt = db.select(Books).order_by(Books.id)
        results = db.session.execute(stmt)
        return results.scalars().all()


def get_book(book_id):
    with app.app_context():
        stmt = db.select(Books).where(Books.id == book_id)
        result = db.session.execute(stmt)
        return result.scalars().first()


def add_book(book_name, book_author, book_rating):
    with app.app_context():
        new_book = Books(title=book_name, author=book_author, rating=book_rating)
        db.session.add(new_book)
        db.session.commit()


def update_book_rating(book_id, new_rating):
    with app.app_context():
        book = db.session.get(Books, book_id)
        if book:
            book.rating = new_rating
            db.session.commit()


@app.route('/')
def home():
    return render_template('index.html', books=get_all_books())


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = BookForm()
    if form.validate_on_submit():
        try:
            book_name = form.book_name.data
            book_author = form.book_author.data
            book_rating = form.book_rating.data
            add_book(book_name, book_author, book_rating)
            flash('Book successfully added!', 'success')
            return redirect(url_for('add'))
        except IntegrityError:
            db.session.rollback()  # Roll back the session to a clean state
            flash('A book with this title already exists. Please use a different title.', 'danger')
    return render_template('add.html', form=form)


@app.route('/edit-rating/<int:book_id>', methods=['GET', 'POST'])
def edit_rating(book_id):
    form = EditRatingForm()
    if form.validate_on_submit():
        update_book_rating(book_id, form.rating.data)
        return redirect(url_for('home'))
    return render_template('edit_rating.html', form=form, book=get_book(book_id))


@app.route('/delete-book/<int:book_id>')
def delete_book(book_id):
    with app.app_context():
        book_to_delete = db.session.get(Books, book_id)
        if book_to_delete:
            db.session.delete(book_to_delete)
            db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    # Create table
    with app.app_context():
        db.create_all()

    app.run(debug=True)
