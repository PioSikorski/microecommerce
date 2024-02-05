from fastapi.testclient import TestClient
from sqlmodel import Session

from src.product.app.api.model import ProductCreate, ProductUpdate
from src.tests.utils import random_lower_string, random_float, random_int
from src.product.app.api import crud


def test_create_product_superuser(client: TestClient) -> None:
    name = random_lower_string()
    description = random_lower_string()
    category = random_lower_string()
    price = random_float()
    quantity = random_int()
    data = {"name": name, "description": description, "category": category, "price": price, "quantity": quantity}
    response = client.post('/products/', json=data)
    assert 200 <= response.status_code < 300
    product = response.json()
    assert product["name"] == name
    assert product["description"] == description
    assert product["category"] == category
    assert product["price"] == price
    assert product["quantity"] == quantity
    assert "id" in product
    

def test_create_product_normal_user(client: TestClient) -> None:
    name = random_lower_string()
    description = random_lower_string()
    category = random_lower_string()
    price = random_float()
    quantity = random_int()
    data = {"name": name, "description": description, "category": category, "price": price, "quantity": quantity}
    response = client.post('/products/', json=data)
    assert response.status_code == 401


def test_read_products_by_category(client: TestClient, session: Session) -> None:
    for i in range(2):
        name = random_lower_string()
        description = random_lower_string()
        category = "toys"
        price = random_float()
        quantity = random_int()
        product_in = ProductUpdate(name=name, description=description, category=category, price=price, quantity=quantity)
        crud.product.create(db=session, obj_in=product_in)
    response = client.get(f'/products/category/{category}')
    all_products = response.json()
    assert len(all_products) > 1
    for product in all_products:
        assert "name" in product
    

def test_read_product_by_name(client: TestClient, session: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    category = random_lower_string()
    price = random_float()
    quantity = random_int()
    product_in = ProductCreate(name=name, description=description, category=category, price=price, quantity=quantity)
    product = crud.product.create(db=session, obj_in=product_in)
    name = product.name
    response = client.get(f'/products/{name}')
    assert 200 <= response.status_code < 300
    api_product = response.json()
    existing_product = crud.product.get_by_name(db=session, name=name)
    assert existing_product
    assert existing_product.name == api_product["name"]
    
    
def test_update_product_superuser(client: TestClient, session: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    category = random_lower_string()
    price = random_float()
    quantity = random_int()
    product_in = ProductCreate(name=name, description=description, category=category, price=price, quantity=quantity)
    product = crud.product.create(db=session, obj_in=product_in)
    category_update = random_lower_string()
    id = product.id
    data = {"category": category_update}
    response = client.put(f'/products/{id}', json=data)
    assert 200 <= response.status_code < 300
    updated_product = response.json()
    assert product.category == updated_product["category"]


def test_update_product_normal_user(client: TestClient, session: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    category = random_lower_string()
    price = random_float()
    quantity = random_int()
    product_in = ProductCreate(name=name, description=description, category=category, price=price, quantity=quantity)
    product = crud.product.create(db=session, obj_in=product_in)
    category_update = random_lower_string()
    id = product.id
    data = {"category": category_update}
    response = client.put(f'/products/{id}', json=data)
    assert response.status_code == 401


def test_read_products(client: TestClient, session: Session) -> None:
    for i in range(2):
        name = random_lower_string()
        description = random_lower_string()
        category = random_lower_string()
        price = random_float()
        quantity = random_int()
        product_in = ProductUpdate(name=name, description=description, category=category, price=price, quantity=quantity)
        crud.product.create(db=session, obj_in=product_in)
    response = client.get('/products/')
    all_products = response.json()
    assert len(all_products) > 1
    for product in all_products:
        assert "name" in product