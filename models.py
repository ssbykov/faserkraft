from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


Base = declarative_base()
engine = create_engine(f"postgresql://"
                       f"{os.getenv('DB_USER')}"
                       f":{os.getenv('DB_PASS')}"
                       f"@{os.getenv('DB_HOST')}"
                       f":{os.getenv('DB_PORT')}"
                       f"/{os.getenv('DB_BASE')}")
Session = sessionmaker(engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    creation_date = Column(DateTime(), server_default=func.now())
    psw = Column(String(200), nullable=False)


Base.metadata.create_all(engine)


class DB:

    def get_user(self, session, user_id):
        user = session.query(User).get(user_id)
        if user is None:
            raise HttpError(404, 'Пользователя не существуйет!')
        return user

    def get_user_by_mail(self, session, email):
        user = list(session.query(User).filter(User.email == email))
        if user:
            return user[0]
