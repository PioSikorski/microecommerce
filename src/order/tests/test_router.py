import pytest
from fastapi.testclient import TestClient
from pymongo.collection import Collection

from src.order.app.api.crud import crud


@pytest.mark.asyncio
async def test_read_orders_superuser(client: TestClient, db: Collection, superuser_token_headers) -> None:
    for i in range(3):
        obj_in = {"user_id": i, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
        await crud.create(db=db, obj_in=obj_in)
    response = client.get("/orders/", headers=superuser_token_headers)
    assert response.status_code == 200
    orders = response.json()
    assert len(orders) == 3
    
    
@pytest.mark.asyncio
async def test_read_orders_normal_user(client: TestClient, db: Collection, normal_user_token_headers) -> None:
    obj_in = {"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    await crud.create(db=db, obj_in=obj_in)
    response = client.get("/orders/", headers=normal_user_token_headers)
    assert response.status_code == 401
    

@pytest.mark.asyncio
async def test_read_order_superuser(client: TestClient, db: Collection, superuser_token_headers) -> None:
    existing_order = await crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.get(f"/orders/{id}", headers=superuser_token_headers)
    assert response.status_code == 200
    order = response.json()
    assert order["_id"] == str(id)
    

@pytest.mark.asyncio
async def test_read_order_normal_user(client: TestClient, db: Collection, normal_user_token_headers) -> None:
    existing_order = await crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.get(f"/orders/{id}", headers=normal_user_token_headers)
    assert response.status_code == 200
    order = response.json()
    assert order["_id"] == str(id)
    assert order["user_id"] == 2
    

@pytest.mark.asyncio
async def test_read_order_wrong_user(client: TestClient, db: Collection, normal_user_token_headers) -> None:
    existing_order = await crud.create(db=db, obj_in={"user_id": 4, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.get(f"/orders/{id}", headers=normal_user_token_headers)
    assert response.status_code == 401
    

# @pytest.mark.asyncio
# async def test_read_order_products_superuser(client: TestClient, db: Collection, superuser_token_headers) -> None:
#     existing_order = await crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
#     id = existing_order["_id"]
#     response = client.get(f"/orders/{id}/products", headers=superuser_token_headers)
#     assert response.status_code == 200
    

@pytest.mark.asyncio
async def test_order_by_status_superuser(client: TestClient, db: Collection, superuser_token_headers) -> None:
    for i in range(3):
        obj_in = {"user_id": i, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
        await crud.create(db=db, obj_in=obj_in)
    response = client.get("/orders/status/pending", headers=superuser_token_headers)
    assert response.status_code == 200
    orders = response.json()
    assert len(orders) == 3
    

@pytest.mark.asyncio    
async def test_order_by_status_normal_user(client: TestClient, db: Collection, normal_user_token_headers) -> None:
    existing_order = await crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    response = client.get(f"/orders/status/pending", headers=normal_user_token_headers)
    assert response.status_code == 401
    

@pytest.mark.asyncio  
async def test_create_order(client: TestClient, db: Collection, normal_user_token_headers) -> None:
    data = {"shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    response = client.post("/orders/", headers=normal_user_token_headers, json=data)
    created_order = await crud.get(db=db, id=response.json()["_id"])
    assert response.status_code == 200
    order = response.json()
    assert order["status"] == "pending"
    assert str(created_order['_id']) == order['_id']
    

@pytest.mark.asyncio
async def test_update_order_normal_user(client: TestClient, db: Collection, normal_user_token_headers) -> None:
    existing_order = await crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    data = {"status": "shipped"}
    response = client.put(f"/orders/{id}", headers=normal_user_token_headers, json=data)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_order_superuser(client: TestClient, db: Collection, superuser_token_headers) -> None:
    existing_order = await crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    data = {"status": "shipped"}
    response = client.put(f"/orders/{id}", headers=superuser_token_headers, json=data)
    assert response.status_code == 200
    order = response.json()
    assert order["status"] == "shipped"
    

@pytest.mark.asyncio
async def test_delete_order(client: TestClient, db: Collection, normal_user_token_headers) -> None:
    existing_order = await crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.delete(f"/orders/{id}", headers=normal_user_token_headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}
    

@pytest.mark.asyncio
async def test_delete_order_superuser(client: TestClient, db: Collection, superuser_token_headers) -> None:
    existing_order = await crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.delete(f"/orders/{id}", headers=superuser_token_headers)
    assert response.status_code == 200
    deleted_order = response.json()
    assert deleted_order["_id"] == str(id)