from flask import url_for, redirect, request
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from models import User, db


def user_check(current_user):
    if current_user.is_authenticated:
        user_profile = current_user.get_user()
        return current_user.is_authenticated and user_profile.is_admin and user_profile.is_active

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return user_check(current_user)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class MyModelView(ModelView):
    def is_accessible(self):
        return user_check(current_user)

    def inaccessible_callback(self, name, **kwargs):
         return redirect(url_for('profile', next=request.url))


admin = Admin(index_view=MyAdminIndexView(), name='Фазеркрафт', endpoint='admin')
admin.add_view(MyModelView(User, db.session, name='Пользователь'))

