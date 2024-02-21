import requests
import pytest

from src.tests.utils import random_lower_string, random_float, random_int


@pytest.fixture()
def populate_db() -> None:
    superuser_response = requests.post("http://localhost:8000/login/access-token", data={"username": "admin@admin.com", "password": "admin"})
    superuser_token = superuser_response.json()
    headers_superuser = {"Authorization": f"Bearer {superuser_token['access_token']}"}
    for i in range(5):
        obj_in = {"name": random_lower_string(), "description": random_lower_string(), "category": "toys", "quantity": random_int(), "price": random_float()}
        requests.post("http://localhost:8001/products/", headers=headers_superuser, json=obj_in)


def test_user_buys_product(populate_db) -> None:
    user_response = requests.post("http://localhost:8000/users/create", json={"email": "tescior@test.com", "password": "tescior"})
    assert user_response.status_code == 200
    user_token = requests.post("http://localhost:8000/login/access-token", data={"username": "tescior@test.com", "password": "tescior"})
    assert user_token.status_code == 200
    user_header = {"Authorization": f"Bearer {user_token.json()['access_token']}"}
    produts_response = requests.get("http://localhost:8001/products/")
    assert produts_response.status_code == 200
    products = produts_response.json()
    assert len(products) == 5
    product = products[0]
    product_id = product["id"]
    assert product["quantity"] >= 3
    product_price = product["price"]
    user_change_password_response = requests.put("http://localhost:8000/users/me", headers=user_header, json={"password": "test"})
    assert user_change_password_response.status_code == 200
    user_me_response = requests.get("http://localhost:8000/users/me", headers=user_header)
    assert user_me_response.status_code == 200
    shopping_cart_response = requests.post("http://localhost:8003/carts", headers=user_header, json={"products": [{"product_id": product_id, "quantity": 3, "unit_price": product_price}]}) 
    assert shopping_cart_response.status_code == 200
    shopping_cart_id = shopping_cart_response.json()["_id"]
    order_response = requests.post("http://localhost:8002/orders", headers=user_header, json={"shoppingcart_id": shopping_cart_id, "address": "test address", "phone": "123456789"})
    assert order_response.status_code == 200
    order = order_response.json()
    assert order["status"] == "pending"
    assert order["address"] == "test address"
    assert order["phone"] == "123456789"
    assert order["user_id"] == user_response.json()["id"]
    user_orders = requests.get(f"http://localhost:8000/users/me/orders", headers=user_header)
    assert user_orders.status_code == 200
    assert order["_id"] in user_orders.json()
    user_product_change = requests.get(f"http://localhost:8001/products/id/{product_id}")
    assert user_product_change.status_code == 200
    assert user_product_change.json()["quantity"] == product["quantity"] - 3
   
    
    