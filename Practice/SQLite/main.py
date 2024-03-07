# import sqlite3

# # Create a connection to the database
# connection = sqlite3.connect('data.db')

# # Create a cursor object
# cursor = connection.cursor()

# # Create table
# cursor.execute(
#     'CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title VARCHAR(250) NOT NULL UNIQUE, author VARCHAR(250) NOT NULL, rating FLOAT NOT NULL)'
# )

# # Add data to table
# cursor.execute(
#     'INSERT INTO books (title, author, rating) VALUES ("Harry Potter", "J.K. Rowling", 9)'
# )
# connection.commit()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


# configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///new-books-collection.db'  # "sqlite:///<name of database>.db"
)

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


# Create table
with app.app_context():
    db.create_all()

# Add data to table
with app.app_context():
    # primary key field is optional. id field will be auto-generated if left empty.
    new_book = Books(id=8, title="Harry Potter 8", author="J.K. Rowling", rating=9)
    db.session.add(new_book)
    db.session.commit()

# Read all data from table
with app.app_context():
    # note that Books.<field> will decide sorting i.e. which row data will get printed first in for loop.
    stmt = db.select(Books).order_by(Books.title)
    results = db.session.execute(stmt)
    all_books = results.scalars().all()

    for book in all_books:
        print(book.title, book.rating, book.author)

# Read a particular data from table
with app.app_context():
    stmt = db.select(Books).where(Books.title == "Harry Potter")
    result = db.session.execute(stmt)
    book = result.scalars().first()
    if book:
        print(book.id, book.title, book.rating)

# Update a particular data from table by query
with app.app_context():
    stmt = db.select(Books).where(Books.title == "Harry Potter")
    result = db.session.execute(stmt)
    book = result.scalars().first()
    if book:
        book.title = "Harry Potter and the Chamber of Secrets"
        db.session.commit()

# Update a particular data from table By PRIMARY KEY
book_id = 7
with app.app_context():
    book = db.session.get(Books, book_id)
    if book:
        book.title = "Harry Potter and the Goblet of Fire"
        db.session.commit()

# Delete A Particular Record By PRIMARY KEY
book_id = 8
with app.app_context():
    book_to_delete = db.session.get(Books, book_id)
    # or book_to_delete = db.get_or_404(Book, book_id)
    if book_to_delete:
        db.session.delete(book_to_delete)
        db.session.commit()
