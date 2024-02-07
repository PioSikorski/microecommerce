from pymongo.collection import Collection
from bson.objectid import ObjectId

from src.order.app.api.crud import crud


def test_get(db: Collection) -> None:
    obj_in = {"user_id": 1, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    existing_order = crud.create(db=db, obj_in=obj_in)
    id = existing_order["_id"]
    result = crud.get(db, str(id))
    assert result["_id"] == id 
    assert result["user_id"] == obj_in["user_id"]
    

def test_create(db: Collection) -> None:
    obj_in = {"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    result = crud.create(db, obj_in)
    result = crud.get(db, str(result["_id"]))
    assert "_id" in result
    assert result["user_id"] == obj_in["user_id"]
    assert result["status"] == "pending"


def test_update(db: Collection) -> None:
    obj_in = {"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    existing_order = crud.create(db=db, obj_in=obj_in)
    id = existing_order["_id"]
    result = crud.update(db, str(id), {"status": "shipped"})
    assert result["_id"] == id
    assert result["status"] == "shipped"


def test_delete(db: Collection) -> None:
    obj_in = {"user_id": 1, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    existing_order = crud.create(db=db, obj_in=obj_in)
    id = existing_order["_id"]
    crud.delete(db, str(id))
    assert db.find_one({"_id": id}) is None
    

def test_get_all_by_status(db: Collection) -> None:
    obj_in = {"user_id": 3, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    crud.create(db=db, obj_in=obj_in)
    obj_in1 = {"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    crud.create(db=db, obj_in=obj_in1)
    result = crud.get_all_by_status(db, "pending")
    assert len(result) == 2
    assert result[0]["status"] == "pending"


def test_get_all_by_user(db: Collection) -> None:
    obj_in = {"user_id": 3, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    crud.create(db=db, obj_in=obj_in)
    obj_in1 = {"user_id": 3, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
    crud.create(db=db, obj_in=obj_in1)
    result = crud.get_all_by_user(db, obj_in["user_id"])
    assert len(result) == 2
    assert result[0]["user_id"] == obj_in["user_id"]


def test_get_collection(db: Collection) -> None:
    for i in range(3):
        obj_in = {"user_id": 2, "status": "pending", "shoppingcart_id": "65c8dd402a24d2c9d160d17f", "address": "123 Main St", "phone": "123-456-7890"}
        crud.create(db=db, obj_in=obj_in)
    result = crud.get_collection(db)
    assert len(result) == 3