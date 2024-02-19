from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from src.product.app.api.crud import crud
from src.product.app.api.model import ProductCreate, ProductUpdate
from src.tests.utils import random_float, random_int, random_lower_string


def test_get_product(session: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    category = random_lower_string()
    price = random_float()
    quantity = random_int()
    product_in = ProductCreate(name=name, description=description, category=category, price=price, quantity=quantity)
    product = crud.create(db=session, obj_in=product_in)
    product_get = crud.get(db=session, id=product.id)
    assert product_get
    assert product.id == product_get.id
    assert jsonable_encoder(product) == jsonable_encoder(product_get)


def test_get_product_by_name(session: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    category = random_lower_string()
    price = random_float()
    quantity = random_int()
    product_in = ProductCreate(name=name, description=description, category=category, price=price, quantity=quantity)
    product = crud.create(db=session, obj_in=product_in)
    product_get = crud.get_by_name(db=session, name=name)
    assert product_get
    assert product.name == product_get.name
    assert jsonable_encoder(product) == jsonable_encoder(product_get)


def test_get_product_by_category(session: Session) -> None:
    for i in range(2):
        name = random_lower_string()
        description = random_lower_string()
        category = "toys"
        price = random_float()
        quantity = random_int()
        product_in = ProductCreate(name=name, description=description, category=category, price=price, quantity=quantity)
        crud.create(db=session, obj_in=product_in)
    products = crud.get_category(db=session, category=category)
    assert len(products) > 1
    for product in products:
        assert product.category == "toys"


def test_create_product(session: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    category = random_lower_string()
    price = random_float()
    quantity = random_int()
    product_in = ProductCreate(name=name, description=description, category=category, price=price, quantity=quantity)
    product = crud.create(db=session, obj_in=product_in)
    assert product.name == name
    assert product.description == description
    assert product.category == category
    assert product.price == price
    assert product.quantity == quantity
    assert hasattr(product, "id")


def test_update_product(session: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    category = random_lower_string()
    price = random_float()
    quantity = random_int()
    product_in = ProductCreate(name=name, description=description, category=category, price=price, quantity=quantity)
    product = crud.create(db=session, obj_in=product_in)
    new_description = random_lower_string()
    product_in_update = ProductUpdate(description=new_description)
    crud.update(db=session, db_obj=product, obj_in=product_in_update)
    product_get = crud.get(db=session, id=product.id)
    assert product_get
    assert product.name == product_get.name
    assert description != product_get.description
    

def test_delete_product(session: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    category = random_lower_string()
    price = random_float()
    quantity = random_int()
    product_in = ProductCreate(name=name, description=description, category=category, price=price, quantity=quantity)
    product = crud.create(db=session, obj_in=product_in)
    product_get = crud.get(db=session, id=product.id)
    assert product_get
    deleted_product = crud.remove(db=session, id=product.id)
    product_get = crud.get(db=session, id=product.id)
    assert product_get is None
    assert deleted_product.id == product.id
    assert jsonable_encoder(product) == jsonable_encoder(deleted_product)