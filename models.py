import os
from datetime import datetime, timedelta
from typing import List
import json

from dotenv import load_dotenv
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SQLALCHEMY_DATABASE_URI = f"postgresql://" \
                          f"{os.getenv('DB_USER')}" \
                          f":{os.getenv('DB_PASS')}" \
                          f"@{os.getenv('DB_HOST')}" \
                          f":{os.getenv('DB_PORT')}" \
                          f"/{os.getenv('DB_BASE')}"

db = SQLAlchemy()


class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    creation_date = db.Column(db.DateTime(), default=datetime.now)
    psw = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<users {self.id}>"

    def get_token(self, expire_time=12):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token


# product_stage = db.Table('product_stage',
#                          db.Column('order_num', db.Integer),
#                          db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
#                          db.Column('stage_id', db.Integer, db.ForeignKey('stage.id'))
#                          )
#

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    stages = db.relationship('Stage', secondary='product_stage',
                                  backref=db.backref('products', lazy=True))
    # stages = db.relationship("Stage", secondary='product_stage', back_populates="products")

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    # products = db.relationship("Product", secondary='product_stage', back_populates="stages")

    def __repr__(self):
        return self.name

def order_num_default(context):
    res = context.get_current_parameters()
    return res

class ProductStage(db.Model):
    __tablename__ = 'product_stage'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'), nullable=False)
    order_num = db.Column(db.Integer, nullable=False)

    product = db.relationship(Product, backref='products')
    stage = db.relationship(Stage, backref='stages')

    __table_args__ = (
            CheckConstraint(order_num > 0, name='order_num_con'),
            UniqueConstraint("product_id", "stage_id"),
            UniqueConstraint("product_id", "order_num"),
    )

# class Operation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     num = db.Column(db.Integer, unique=True)
#     name = db.Column(db.String(100), nullable=False, unique=True)
#     operation = db.relationship('Operation', backref=db.backref('execution', lazy='dynamic'))


# class Operation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     stage_id = db.Column(db.Integer, db.ForeignKey(Stage.id), nullable=False)
#     execution_id = db.Column(db.Integer, db.ForeignKey(Execution.id), nullable=False)
#     db.UniqueConstraint(stage_id, execution_id)
# product = db.relationship(Product, backref='operations')
# execution = db.relationship(Execution, back_populates='technologes')


# class Technology(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
#     operation_id = db.Column(db.Integer, db.ForeignKey(Operation.id), nullable=False)
# product = db.relationship(Product, backref='operations')
# execution = db.relationship(Execution, back_populates='technologes')


class Unit(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    product = db.relationship("Product", backref='unit')


# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     unit_id = db.Column(db.Integer, db.ForeignKey(Unit.id), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
# technology_id = db.Column(db.Integer, db.ForeignKey(Technology.id), nullable=False)
# @db.validates('stage_execution_id')
# def validate_name(self, key, value):
#     stage_execution = db.session.query()
#     assert value != ''
#     return value


class DB:

    def get_user(self, user_id):
        user = db.session.query(User).get(user_id)
        if user is None:
            raise HttpError(404, 'Пользователя не существуйет!')
        return user

    def get_user_by_mail(self, email):
        user = db.session.query(User).filter(User.email == email)
        for u in user:
            return u
