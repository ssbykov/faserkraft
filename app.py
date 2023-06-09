import os

from dotenv import load_dotenv
from flask import Flask, url_for, render_template, redirect
from flask_login import LoginManager, login_required, logout_user, current_user

import error_handlers
from UserLogin import UserLogin
from admin import admin
from models import db, SQLALCHEMY_DATABASE_URI
from tests_data import new_base
from views import UserRegister, UserLog, LoginAPI, ProductApi
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.register_blueprint(error_handlers.blueprint)

api = Api(app)
jwt = JWTManager(app)
db.init_app(app)
admin.init_app(app)

with app.app_context():
    # new_base()
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return render_template('base.html')


@app.route('/profile')
@login_required
def profile():
    if current_user.is_authenticated:
        user_profile = current_user.get_user()
        return f"""<a href="{url_for('logout')}">Выйти из профиля</a>
                <p>Данные пользователя: {user_profile.name} {user_profile.surname}
                <p> Администратор: {user_profile.is_admin}"""
    return redirect(url_for('login'))


# @app.errorhandler(404)
# def redirect_404(error):
#     return redirect(url_for('register'))


app.add_url_rule('/reg', view_func=UserRegister.as_view('register'))
app.add_url_rule('/login', view_func=UserLog.as_view('login'))
login_manager.login_message = "Необходима авторизация"
login_manager.login_message_category = "success"

api.add_resource(LoginAPI, '/api/login')
api.add_resource(ProductApi, '/api/product')


if __name__ == '__main__':
    app.run()
