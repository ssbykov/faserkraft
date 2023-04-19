import os

from flask import Flask, url_for, render_template, redirect, jsonify
from dotenv import load_dotenv
from flask_login import LoginManager, login_required, logout_user, current_user

from UserLogin import UserLogin
from models import Session

from views import UserRegister, UserLog

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    with Session() as session:
        return UserLogin().from_db(session, user_id)

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
                Данные пользователя: \n{user_profile.name} \n {user_profile.surname}"""
    return redirect(url_for('login'))


@app.errorhandler(404)
def redirect_404(error):
    return redirect(url_for('register'))


app.add_url_rule('/reg', view_func=UserRegister.as_view('register'))
app.add_url_rule('/login', view_func=UserLog.as_view('login'))
login_manager.login_message = "Необходима авторизация"
login_manager.login_message_category = "success"

if __name__ == '__main__':
    app.run()

# with app.test_request_context():
#     print(url_for('index'))
