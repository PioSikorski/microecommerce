from unittest.mock import patch

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


@pytest.mark.asyncio
async def test_read_order_not_found(client: TestClient, db: Collection, superuser_token_headers) -> None:
    response = client.get("/orders/5f1d8f2b5e8f2e4e3f9c5f1d", headers=superuser_token_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
@patch('requests.get')
async def test_read_order_products_superuser(mock_get, client: TestClient, db: Collection, superuser_token_headers) -> None:
    mock_get.return_value.json.return_value = [{"product_id": 1, "quantity": 2, "unit_price": 10.0}]
    existing_order = await crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.get(f"/orders/{id}/products", headers=superuser_token_headers)
    assert response.status_code == 200


@pytest.mark.asyncio
@patch('requests.get')
async def test_read_order_products_normal_user(mock_get, client: TestClient, db: Collection, normal_user_token_headers) -> None:
    mock_get.return_value.json.return_value = [{"product_id": 1, "quantity": 2, "unit_price": 10.0}]
    existing_order = await crud.create(db=db, obj_in={"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.get(f"/orders/{id}/products", headers=normal_user_token_headers)
    assert response.status_code == 200
 

@pytest.mark.asyncio
@patch('requests.get')
async def test_read_order_products_not_found(mock_get, client: TestClient, db: Collection, superuser_token_headers) -> None:
    mock_get.return_value.json.return_value = {"detail": "Shopping cart not found"}
    response = client.get("/orders/5f1d8f2b5e8f2e4e3f9c5f1d/products", headers=superuser_token_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_read_order_products_wrong_user(client: TestClient, db: Collection, normal_user_token_headers) -> None:
    existing_order = await crud.create(db=db, obj_in={"user_id": 4, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"})
    id = existing_order["_id"]
    response = client.get(f"/orders/{id}/products", headers=normal_user_token_headers)
    assert response.status_code == 401


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
async def test_order_by_status_invalid_status(client: TestClient, db: Collection, superuser_token_headers) -> None:
    response = client.get("/orders/status/invalid", headers=superuser_token_headers)
    assert response.status_code == 400


@pytest.mark.asyncio
@patch('requests.get')
@patch('src.order.app.api.service.product_rpc_client.call')
@patch('src.order.app.api.service.user_rpc_client.call')
async def test_create_order(mock_product_call, mock_user_call, mock_get, client: TestClient, db: Collection, normal_user_token_headers) -> None:
    mock_get.return_value.json.return_value = [{"product_id": 1, "quantity": 2, "unit_price": 10.0}]
    mock_product_call.return_value.json.return_value = {"status": "success", "message": "Products updated successfully"}
    mock_user_call.return_value.json.return_value = {"status": "success", "message": "User updated successfully"}
    data = {"shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    response = client.post("/orders/", headers=normal_user_token_headers, json=data)
    created_order = await crud.get(db=db, id=response.json()["_id"])
    assert response.status_code == 200
    order = response.json()
    assert order["status"] == "pending"
    assert str(created_order['_id']) == order['_id']


@pytest.mark.asyncio
async def test_create_order_no_user(client: TestClient, db: Collection) -> None:
    data = {"shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    response = client.post("/orders/", json=data)
    assert 400 < response.status_code < 500
    assert response.json() == {"detail": "Not authenticated"}


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
async def test_update_order_not_found(client: TestClient, superuser_token_headers) -> None:
    data = {"status": "shipped"}
    response = client.put("/orders/5f1d8f2b5e8f2e4e3f9c5f1d", headers=superuser_token_headers, json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}
    

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
    

@pytest.mark.asyncio
async def test_delete_order_not_found(client: TestClient, superuser_token_headers) -> None:
    response = client.delete("/orders/5f1d8f2b5e8f2e4e3f9c5f1d", headers=superuser_token_headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}