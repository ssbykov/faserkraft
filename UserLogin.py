from models import HttpError, User
from flask_login import UserMixin
from models import db

class UserLogin(UserMixin):
    def from_db(self, user_id):
        user = db.session.query(User).get(user_id)
        if user is None:
            raise HttpError(404, 'Пользователя не существуйет!')
        self.__user = user
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.id)

    def get_user(self):
        return self.__user