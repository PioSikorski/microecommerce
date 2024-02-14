import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockCollection

from src.cart.app.api.crud import crud

@pytest.mark.asyncio
async def test_read_carts_superuser(client: TestClient, db: AsyncMongoMockCollection, superuser_token_headers) -> None:
    for i in range(3):
        user_id = i + 1
        obj_in = {"user_id": user_id, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
        await crud.create(db=db, obj_in=obj_in)
    response = client.get("/carts/", headers=superuser_token_headers)
    assert response.status_code == 200
    carts = response.json()
    assert len(carts) == 3
    
    
@pytest.mark.asyncio
async def test_read_carts_normal_user(client: TestClient, db: AsyncMongoMockCollection, normal_user_token_headers) -> None:
    obj_in = {"user_id": 2, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
    await crud.create(db=db, obj_in=obj_in)
    response = client.get("/carts/", headers=normal_user_token_headers)
    assert response.status_code == 401
    

@pytest.mark.asyncio
async def test_read_cart_superuser(client: TestClient, db: AsyncMongoMockCollection, superuser_token_headers) -> None:
    existing_cart = await crud.create(db=db, obj_in={"user_id": 2, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]})
    id = existing_cart["_id"]
    response = client.get(f"/carts/{id}", headers=superuser_token_headers)
    assert response.status_code == 200
    cart = response.json()
    assert cart["_id"] == str(id)
    

@pytest.mark.asyncio
async def test_read_cart_normal_user(client: TestClient, db: AsyncMongoMockCollection, normal_user_token_headers) -> None:
    existing_cart = await crud.create(db=db, obj_in={"user_id": 2, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]})
    id = existing_cart["_id"]
    response = client.get(f"/carts/{id}", headers=normal_user_token_headers)
    assert response.status_code == 200
    cart = response.json()
    assert cart["_id"] == str(id)
    

@pytest.mark.asyncio
async def test_read_cart_wrong_user(client: TestClient, db: AsyncMongoMockCollection, normal_user_token_headers) -> None:
    existing_cart = await crud.create(db=db, obj_in={"user_id": 4, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]})
    id = existing_cart["_id"]
    response = client.get(f"/carts/{id}", headers=normal_user_token_headers)
    assert response.status_code == 401
    

@pytest.mark.asyncio    
async def test_read_cart_products_superuser(client: TestClient, db: AsyncMongoMockCollection, superuser_token_headers) -> None:
    response = await crud.create(db=db, obj_in={"user_id": 2, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]})
    cart_id = response["_id"]
    response = client.get(f"/carts/{cart_id}/products", headers=superuser_token_headers)
    assert response.status_code == 200
    

@pytest.mark.asyncio
async def test_add_product_superuser(client: TestClient, db: AsyncMongoMockCollection, superuser_token_headers) -> None:
    response = await crud.create(db=db, obj_in={"user_id": 2, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]})
    cart_id = response["_id"]
    response = client.put(f"/carts/{cart_id}/add", json={"product_id": 3, "quantity": 2, "unit_price": 50.0}, headers=superuser_token_headers)
    assert response.status_code == 200
    cart = response.json()
    assert cart["_id"] == str(cart_id)
    assert len(cart["products"]) == 2
    assert cart["products"][0]["product_id"] == 1
    
### NotImplementedError: Array filters are not implemented in mongomock yet.
# @pytest.mark.asyncio
# async def test_update_product_in_order_superuser(client: TestClient, db: AsyncMongoMockCollection, superuser_token_headers) -> None:
#     response = crud.create(db=db, obj_in={"user_id": 2, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]})
#     cart_id = response["_id"]
#     product_id = 1
#     product_in = {"quantity": 3, "unit_price": 60.0}
#     response = client.put(f"/carts/{cart_id}/products/{product_id}", json=product_in, headers=superuser_token_headers)
#     assert response.status_code == 200
#     updated_cart = response.json()
#     assert updated_cart["_id"] == cart_id
#     assert len(updated_cart["products"]) == 1
#     assert updated_cart["products"][0]["product_id"] == product_id
#     assert updated_cart["products"][0]["quantity"] == product_in["quantity"]
#     assert updated_cart["products"][0]["unit_price"] == product_in["unit_price"]


# @pytest.mark.asyncio
# async def test_update_product_in_order_normal_user(client: TestClient, db: AsyncMongoMockCollection, normal_user_token_headers) -> None:
#     response = crud.create(db=db, obj_in={"user_id": 2, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]})
#     cart_id = response["_id"]
#     product_id = 1
#     product_in = {"quantity": 3, "unit_price": 60.0}
#     response = client.put(f"/carts/{cart_id}/products/{product_id}", json=product_in, headers=normal_user_token_headers)
#     assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_cart_normal_user(client: TestClient, db: AsyncMongoMockCollection, normal_user_token_headers) -> None:
    existing_cart = await crud.create(db=db, obj_in={"user_id": 2, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]})
    id = existing_cart["_id"]
    response = client.delete(f"/carts/{id}", headers=normal_user_token_headers)
    assert response.status_code == 200
    cart = response.json()
    assert cart["_id"] == str(id)
    get_cart = await crud.get(db=db, id=id)
    assert get_cart is None
    

@pytest.mark.asyncio
async def test_delete_cart_superuser(client: TestClient, db: AsyncMongoMockCollection, superuser_token_headers) -> None:
    existing_cart = await crud.create(db=db, obj_in={"user_id": 2, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]})
    id = existing_cart["_id"]
    response = client.delete(f"/carts/{id}", headers=superuser_token_headers)
    assert response.status_code == 200
    cart = response.json()
    assert cart["_id"] == str(id)
    get_cart = await crud.get(db=db, id=id)
    assert get_cart is None
    
 
@pytest.mark.asyncio   
async def test_delete_cart_wrong_user(client: TestClient, db: AsyncMongoMockCollection, normal_user_token_headers) -> None:
    existing_cart = await crud.create(db=db, obj_in={"user_id": 4, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]})
    id = existing_cart["_id"]
    response = client.delete(f"/carts/{id}", headers=normal_user_token_headers)
    assert response.status_code == 401