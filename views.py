from flask.views import MethodView

from UserLogin import UserLogin
from forms import RegistrationForm, LogForm
from models import User, DB
from flask import request, render_template, flash, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from models import db

class UserLog(MethodView):
    def __init__(self):
        self.form = LogForm()
        self.temp = 'login.html'

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('profile'))
        return render_template(self.temp, form=self.form)

    def post(self):
        user_data = request.form
        if self.form.validate_on_submit():
            user = DB().get_user_by_mail(user_data['email'])
            if user and check_password_hash(user.psw, request.form['password']):
                userlogin = UserLogin().create(user)
                login_user(userlogin)
                return redirect(url_for('profile'))

            flash("Неверная пара логин/пароль", "error")

        return render_template(self.temp, form=self.form)


class UserRegister(MethodView):
    def __init__(self):
        self.form = RegistrationForm()
        self.temp = 'register.html'

    def get(self):
        return render_template(self.temp, form=self.form)

    def post(self):
        user_data = request.form
        if self.form.validate_on_submit():
            hash_psw = generate_password_hash(user_data['password'])
            try:
                new_user = User(
                    name=user_data['name'],
                    surname=user_data['surname'],
                    email=user_data['email'],
                    psw=hash_psw
                )
                db.session.add(new_user)
                db.session.flush()
                db.session.commit()
                flash('Новый пользователь создан!', category='success')
                return redirect(url_for('login'))
            except:
                db.session.rollback()
                flash('Ошибка добавление в БД!', category='error')
        return render_template(self.temp, form=self.form)
