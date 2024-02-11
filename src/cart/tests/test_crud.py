from pymongo.collection import Collection

from src.cart.app.api.crud import crud


def test_get(db: Collection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
    id = db.insert_one(obj_in).inserted_id
    result = crud.get(db, id)
    assert result["_id"] == id
    assert result["user_id"] == 1
    

def test_create(db: Collection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
    result = crud.create(db, obj_in)
    assert "_id" in result
    assert result["user_id"] == 1
    assert result["total_amount"] == 100.0
    

def test_update(db: Collection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
    id = db.insert_one(obj_in).inserted_id
    result = crud.update(db, id, {"total_amount": 200.0})
    assert result["_id"] == id
    assert result["total_amount"] == 200.0


def test_delete(db: Collection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
    id = db.insert_one(obj_in).inserted_id
    crud.delete(db, str(id))
    assert db.find_one({"_id": id}) is None
    
    
def test_get_collection(db: Collection) -> None:
    for i in range(3):
        obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
        db.insert_one(obj_in)
    result = crud.get_collection(db)
    assert len(result) == 3
    for i in range(3):
        assert result[i]["user_id"] == 1
        

def test_add_product(db: Collection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
    id = db.insert_one(obj_in).inserted_id
    result = crud.add_product(db, id, {"product_id": 3, "quantity": 2, "unit_price": 50.0})
    assert result["_id"] == id
    assert len(result["products"]) == 2
    assert result["products"][0]["product_id"] == 1
    
    
###  NotImplementedError: Array filters are not implemented in mongomock yet.
# def test_update_product(db: Collection) -> None:
#     obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}]}
#     id = db.insert_one(obj_in).inserted_id
#     product_update = {"quantity": 3}
#     updated_product = crud.update_product(db, id, 1, product_update)
#     assert updated_product["_id"] == id
#     assert updated_product["products"][0]["quantity"] == 3
    
    
def test_remove_product(db: Collection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}, {"product_id": 2, "quantity": 2, "unit_price": 50.0}]}
    id = db.insert_one(obj_in).inserted_id
    product_id = obj_in["products"][0]["product_id"]
    result = crud.remove_product(db, id, product_id)
    assert result["_id"] == id
    assert len(result["products"]) == 1
    
    
def test_remove_all_products(db: Collection) -> None:
    obj_in = {"user_id": 1, "total_amount": 100.0, "products": [{"product_id": 1, "quantity": 2, "unit_price": 50.0}, {"product_id": "2", "quantity": 2, "unit_price": 50.0}]}
    id = db.insert_one(obj_in).inserted_id
    result = crud.remove_all_products(db, str(id))
    assert result["_id"] == id
    assert len(result["products"]) == 0