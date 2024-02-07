from fastapi.testclient import TestClient
from pymongo.collection import Collection

from src.order.app.api.crud import crud


def test_read_orders_superuser(client: TestClient, db: Collection) -> None:
    for i in range(3):
        obj_in = {"user_id": i, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
        crud.create(db=db, obj_in=obj_in)
    response = client.get("/orders/")
    assert response.status_code == 200
    orders = response.json()
    assert len(orders["orders"]) == 3
    

def test_read_orders_normal_user(client: TestClient, db: Collection) -> None:
    obj_in = {"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    crud.create(db=db, obj_in=obj_in)
    response = client.get("/orders/")
    assert response.status_code == 401
    

def test_read_order_superuser(client: TestClient, db: Collection) -> None:
    existing_order = crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.get(f"/orders/{id}")
    assert response.status_code == 200
    order = response.json()
    assert order["_id"] == str(id)
    
    
def test_read_order_normal_user(client: TestClient, db: Collection) -> None:
    existing_order = crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.get(f"/orders/{id}")
    assert response.status_code == 200
    order = response.json()
    assert order["_id"] == str(id)
    assert order["user_id"] == 2
    

def test_read_order_wrong_user(client: TestClient, db: Collection) -> None:
    existing_order = crud.create(db=db, obj_in={"user_id": 4, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.get(f"/orders/{id}")
    assert response.status_code == 401
    

# def test_read_order_products_superuser(client: TestClient, db: Collection) -> None:
#     existing_order = crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
#     id = existing_order["_id"]
#     response = client.get(f"/orders/{id}/products")
#     assert response.status_code == 200
    

def test_order_by_status_superuser(client: TestClient, db: Collection) -> None:
    for i in range(3):
        obj_in = {"user_id": i, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
        crud.create(db=db, obj_in=obj_in)
    response = client.get("/orders/status/pending")
    assert response.status_code == 200
    orders = response.json()
    assert len(orders) == 3
    
    
def test_order_by_status_normal_user(client: TestClient, db: Collection) -> None:
    existing_order = crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    response = client.get(f"/orders/status/pending")
    assert response.status_code == 401
    
    
def test_create_order(client: TestClient, db: Collection) -> None:
    data = {"shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    response = client.post("/orders/", json=data)
    created_order = crud.get(db=db, id=response.json()["_id"])
    assert response.status_code == 200
    order = response.json()
    assert order["status"] == "pending"
    assert str(created_order['_id']) == order['_id']
    

def test_update_order_normal_user(client: TestClient, db: Collection) -> None:
    existing_order = crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    data = {"status": "shipped"}
    response = client.put(f"/orders/{id}", json=data)
    assert response.status_code == 403


def test_update_order_superuser(client: TestClient, db: Collection) -> None:
    existing_order = crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    data = {"status": "shipped"}
    response = client.put(f"/orders/{id}", json=data)
    assert response.status_code == 200
    order = response.json()
    assert order["status"] == "shipped"
    

def test_delete_order(client: TestClient, db: Collection) -> None:
    existing_order = crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.delete(f"/orders/{id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}
    

def test_delete_order_superuser(client: TestClient, db: Collection) -> None:
    existing_order = crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.delete(f"/orders/{id}")
    assert response.status_code == 200
    assert response.json() == True