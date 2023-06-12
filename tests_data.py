from werkzeug.security import generate_password_hash

from models import Stage, Product, ProductStage, User, db, Unit


def new_base():
    dict_models = {
        "Stage": Stage,
        "Product": Product,
        "ProductStage": ProductStage,
        "User": User,
        "Unit": Unit,
    }
    db.drop_all()
    db.create_all()
    for line in data:
        if line.get("fields").get("psw"):
            line["fields"]["psw"] = generate_password_hash(line["fields"]["psw"])
        db.session.add(dict_models[line.get("model")](**line.get("fields")))
    db.session.commit()


data = [
    {"model": "Stage", "pk": 1, "fields": {"name": "Склеивание корпуса"}},
    {"model": "Stage", "pk": 2, "fields": {"name": "Наполнение волокном"}},
    {"model": "Stage", "pk": 3, "fields": {"name": "Проверка на стенде"}},
    {"model": "Stage", "pk": 4, "fields": {"name": "Упаковка"}},
    {"model": "Product", "pk": 1, "fields": {"name": "Фильтр 1"}},
    {"model": "Product", "pk": 2, "fields": {"name": "Фильтр 2"}},
    {"model": "Product", "pk": 3, "fields": {"name": "Фильтр 3"}},
    {"model": "ProductStage", "pk": 1, "fields": {"product_id": 1, "stage_id": 1, "order_num": 1}},
    {"model": "ProductStage", "pk": 2, "fields": {"product_id": 1, "stage_id": 2, "order_num": 2}},
    {"model": "ProductStage", "pk": 3, "fields": {"product_id": 2, "stage_id": 1, "order_num": 1}},
    {"model": "ProductStage", "pk": 4, "fields": {"product_id": 2, "stage_id": 2, "order_num": 2}},
    {"model": "ProductStage", "pk": 5, "fields": {"product_id": 3, "stage_id": 1, "order_num": 1}},
    {"model": "ProductStage", "pk": 6, "fields": {"product_id": 3, "stage_id": 2, "order_num": 2}},
    {"model": "Unit", "fields": {"product_id": 3, "code": "uf_0000001"}},
    {"model": "Unit", "fields": {"product_id": 1, "code": "uf_0000002"}},
    {"model": "Unit", "fields": {"product_id": 2, "code": "uf_0000020"}},
    {"model": "Unit", "fields": {"product_id": 3, "code": "uf_0000011"}},
    {"model": "User", "fields": {
        "name": "Сергей",
        "surname": "Быков",
        "email": "ss.bykoff@gmail.com",
        "psw": "123456",
        "is_admin": True
    }}
]
