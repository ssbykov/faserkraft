from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import Length, DataRequired, Email, EqualTo

from models import DB


class RegistrationForm(FlaskForm):
    name = StringField('Имя', [DataRequired(), Length(min=2, max=25)])
    surname = StringField('Фамилия', [DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', [DataRequired(), Email('Некорректный email')])
    password = PasswordField('Пароль', [
        DataRequired(), Length(min=6, max=10),
        EqualTo('confirm', message='Пароли должны совпадать')
    ])
    confirm = PasswordField('Повтор пароля', [DataRequired(), Length(min=6, max=10)])
    submit = StringField('Отправить')

    @staticmethod
    def validate_email(form, field):
        if DB().get_user_by_mail(field.data):
            raise ValidationError('Пользователь с данным "email" уже существует!')


class LogForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Пароль', [DataRequired()])
    submit = StringField('Войти')
