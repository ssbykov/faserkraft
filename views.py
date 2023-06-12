from flask import request, render_template, flash, url_for, redirect
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_login import login_user, current_user
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from UserLogin import UserLogin
from forms import RegistrationForm, LogForm
from models import User, DB, Unit
from models import db


class LoginAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = DB().get_user(user_id)
        if user.is_active:
            return {'user': user_id, 'name': user.name}
        return {405: ("Учетная запись не активна", "error")}

    def post(self):
        user = self.get_identity_if_logedin()
        if user:
            pass
        user_data = request.form
        user = DB().get_user_by_mail(user_data['email'])
        if user and check_password_hash(user.psw, request.form['password']):
            if user.is_active:
                token = user.get_token()
                return {'access_token': token, 201: ("Вы вошли в систему", "success")}
            return {405: ("Учетная запись не активна", "error")}
        return {401: ("Неверная пара логин/пароль", "error")}

    def get_identity_if_logedin(self):
        try:
            verify_jwt_in_request()
            return get_jwt_identity()
        except Exception:
            pass


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
                if user.is_active:
                    userlogin = UserLogin().create(user)
                    login_user(userlogin)
                    return redirect(url_for('profile'))
                flash("Учетная запись не активна", "error")
            else:
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


class ProductApi(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = DB().get_user(user_id)
        if user.is_active:
            unit_code = request.values.get('product')
            unit = db.session.query(Unit).get(unit_code)
            if unit:
                return {'code': unit.code, 'name': unit.product.name}
            return {'code': None, 'name': None}
        return {405: ("Учетная запись не активна", "error")}

