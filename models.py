import os
from datetime import datetime

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SQLALCHEMY_DATABASE_URI = f"postgresql://" \
                          f"{os.getenv('DB_USER')}" \
                          f":{os.getenv('DB_PASS')}" \
                          f"@{os.getenv('DB_HOST')}" \
                          f":{os.getenv('DB_PORT')}" \
                          f"/{os.getenv('DB_BASE')}"

db = SQLAlchemy()


class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    creation_date = db.Column(db.DateTime(), default=datetime.now)
    psw = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<users {self.id}>"


class DB:

    def get_user(self, session, user_id):
        user = session.query(User).get(user_id)
        if user is None:
            raise HttpError(404, 'Пользователя не существуйет!')
        return user

    def get_user_by_mail(self, email):
        user = db.session.query(User).filter(User.email == email)
        for u in user:
            return u
