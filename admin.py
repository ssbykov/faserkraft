from flask import url_for, redirect, request
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from models import User, db, Stage, Product, ProductStage  # , Execution, Operation, Unit


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

# class ChildView(ModelView):
    # form_columns = ('id',)
    # column_display_all_relations = True
    # inline_models = (
    #     Product,)
    # form_columns = ['product_id']
    # column_list = [c_attr.key for c_attr in db.inspect(Technology).mapper.column_attrs]
    # column_list = ('id', 'product_id', 'stage_id', 'execution_id')

class ProductAdmin(ModelView):
    column_labels = dict(name='Название', stages='Этапы')
    column_list = ('id', 'name')
    form_columns = ('name', 'stages')
    inline_models = ((
                         ProductStage,
                         {
                             'column_labels': dict(order_num='Номер', stage='Этап'),
                             'form_columns': ('id', 'order_num', 'stage'),
                         }
                     ),)

    # column_display_all_relations = True
    # column_list = [c_attr.key for c_attr in db.inspect(Technology).mapper.column_attrs]

class TechnologyAdmin(ModelView):
    column_labels = dict(id='Номер', name='Название')
    column_default_sort = 'id'
    column_list = ['id', 'name']
    form_columns = ['id', 'name']
    # form_create_rules = ['name']

admin = Admin(index_view=MyAdminIndexView(), name='Фазеркрафт', endpoint='admin')
admin.add_view(MyModelView(User, db.session, name='Пользователь'))
admin.add_view(ProductAdmin(Product, db.session, name='Продукт'))
admin.add_view(TechnologyAdmin(Stage, db.session, name='Технологический этап'))
# admin.add_view(TechnologyAdmin(Technology, db.session, name='Технология'))
# admin.add_view(OperationAdmin(Operation, db.session, name='Операция'))
# admin.add_view(MyModelView(Execution, db.session, name='Операция'))
# admin.add_view(MyModelView(Unit, db.session, name='Изделие'))

