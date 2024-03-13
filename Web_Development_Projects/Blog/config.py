import os

class Config:
    SECRET_KEY = os.environ.get('CSRF_KEY')
    MY_EMAIL = os.environ.get('MY_EMAIL')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///posts.db'
