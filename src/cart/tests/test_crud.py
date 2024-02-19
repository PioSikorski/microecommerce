import pytest
from mongomock_motor import AsyncMongoMockCollection

from src.cart.app.api.crud import crud


@pytest.mark.asyncio
async def test_get(db: AsyncMongoMockCollection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
    response = await db.insert_one(obj_in)
    id = response.inserted_id
    result = await crud.get(db, id)
    assert result["_id"] == id
    assert result["user_id"] == 1
    
    
@pytest.mark.asyncio    
async def test_get_all(db: AsyncMongoMockCollection) -> None:
    for i in range(3):
        obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
        await db.insert_one(obj_in)
    result = await crud.get_all(db)
    assert len(result) == 3
    for i in range(3):
        assert result[i]["user_id"] == 1
    
    
@pytest.mark.asyncio
async def test_create(db: AsyncMongoMockCollection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
    response = await crud.create(db, obj_in)
    assert "_id" in response
    assert response["user_id"] == 1
    assert response["total_amount"] == 100.0
    
    
@pytest.mark.asyncio
async def test_update(db: AsyncMongoMockCollection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
    response = await db.insert_one(obj_in)
    id = response.inserted_id
    result = await crud.update(db, id, {"total_amount": 200.0})
    assert result["_id"] == id
    assert result["total_amount"] == 200.0


@pytest.mark.asyncio
async def test_remove(db: AsyncMongoMockCollection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
    response = await db.insert_one(obj_in)
    id = response.inserted_id
    result = await crud.remove(db, str(id))
    assert result["_id"] == id
    removed_obj = await db.find_one({"_id  ": id})
    assert removed_obj is None
  
        
@pytest.mark.asyncio
async def test_add_product(db: AsyncMongoMockCollection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
    response = await db.insert_one(obj_in)
    id = response.inserted_id
    result = await crud.add_product(db, id, {"product_id": 3, "quantity": 2, "unit_price": 50.0})
    assert result["_id"] == id
    assert len(result["products"]) == 2
    assert result["products"][0]["product_id"] == 1
    
    
# NotImplementedError: Array filters are not implemented in mongomock yet.   
# @pytest.mark.asyncio
# async def test_update_product(db: AsyncMongoMockCollection) -> None:
#     obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
#     response = await db.insert_one(obj_in)
#     id = response.inserted_id
#     product_update = {"quantity": 3}
#     updated_product = await crud.update_product(db, id, 1, product_update)
#     assert updated_product["_id"] == id
#     assert updated_product["products"][0]["quantity"] == 3
    
    
@pytest.mark.asyncio    
async def test_remove_product(db: AsyncMongoMockCollection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}, {"product_id": 2, "quantity": 2, "unit_price": 50.0}]}
    response = await db.insert_one(obj_in)
    id = response.inserted_id
    product_id = obj_in["products"][0]["product_id"]
    result = await crud.remove_product(db, obj_in, product_id)
    assert result["_id"] == id
    assert len(result["products"]) == 1
  
    
@pytest.mark.asyncio    
async def test_remove_all_products(db: AsyncMongoMockCollection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}, {"product_id": "2", "quantity": 2, "unit_price": 50.0}]}
    response = await db.insert_one(obj_in)
    id = response.inserted_id
    result = await crud.remove_all_products(db, str(id))
    assert result["_id"] == id
    assert len(result["products"]) == 0