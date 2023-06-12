from flask import current_app, flash
from flask import url_for, redirect, request
from flask_admin import Admin, AdminIndexView
from flask_admin._compat import text_type
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView, form
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from models import User, db, Stage, Product, ProductStage, Unit  # , Execution, Operation, Unit


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


class ProductAdmin(ModelView):
    column_labels = dict(name='Название', stages='Этапы', ProductStage='Этап')
    column_list = ('id', 'name')
    form_columns = ('name', 'stages')
    inline_models = ((
                         ProductStage,
                         {
                             'form_label': 'Этап',
                             'column_labels': dict(order_num='Номер', stage='Название'),
                             'form_columns': ('id', 'order_num', 'stage'),
                         }
                     ),)

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        # self._check_date(form.data.get('products'))

    def _check_date(self, products):
        if products:
            self.change_form_products = {}
            order_nums = [product['order_num'] for product in products]
            self.change_form_products['order_num'] = [str(num) for num in set(order_nums) if order_nums.count(num) > 1]
            stages = [product['stage'].name for product in products]
            self.change_form_products['stage'] = [stage for stage in set(stages) if stages.count(stage) > 1]

    # def handle_view_exception(self, exc):
    #     if isinstance(exc, IntegrityError):
    #         if current_app.config.get(
    #                 'ADMIN_RAISE_ON_INTEGRITY_ERROR',
    #                 current_app.config.get('ADMIN_RAISE_ON_VIEW_EXCEPTION')
    #         ):
    #             raise
    #         else:
    #             error_txt = gettext('Integrity error. %(message)s', message=text_type(exc))
    #             if 'UniqueViolation' in text_type(exc):
    #                 if 'order_num' in exc.orig.diag.message_detail:
    #                     order_num = self.change_form_products['order_num']
    #                     error_txt = f"Обнаружено дублирование номеров этапов: {', '.join(order_num)}."
    #                 elif 'stage_id' in exc.orig.diag.message_detail:
    #                     stage = self.change_form_products['stage']
    #                     error_txt = f"Обнаружено дублирование этапов: {', '.join(stage)}."
    #             flash(error_txt, 'error')
    #         return True
    #
    #     return super(ModelView, self).handle_view_exception(exc)

    # column_display_all_relations = True
    # column_list = [c_attr.key for c_attr in db.inspect(Technology).mapper.column_attrs]


class StagesAdmin(ModelView):
    column_labels = dict(id='Номер', name='Название')
    column_default_sort = 'id'
    column_list = ['id', 'name']
    form_columns = ['id', 'name']
    # form_create_rules = ['name']


class UnitAdmin(ModelView):
    column_labels = dict(code='Код', product='Название')


admin = Admin(index_view=MyAdminIndexView(), name='Фазеркрафт', endpoint='admin')
admin.add_view(MyModelView(User, db.session, name='Пользователь'))
admin.add_view(ProductAdmin(Product, db.session, name='Продукт'))
admin.add_view(StagesAdmin(Stage, db.session, name='Технологический этап'))
admin.add_view(UnitAdmin(Unit, db.session, name='Единицы продукции'))
# admin.add_view(TechnologyAdmin(Technology, db.session, name='Технология'))
# admin.add_view(OperationAdmin(Operation, db.session, name='Операция'))
# admin.add_view(MyModelView(Execution, db.session, name='Операция'))
# admin.add_view(MyModelView(Unit, db.session, name='Изделие'))
