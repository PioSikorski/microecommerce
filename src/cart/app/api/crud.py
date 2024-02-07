from pymongo.collection import Collection
from bson.objectid import ObjectId

from src.core.nosql_crud import BaseCRUD


class CartCRUD(BaseCRUD):
    def add_product(self, db: Collection, id: str, obj_in: dict):
        db.update_one({"_id": ObjectId(id)}, {"$push": {"products": obj_in}})
        return db.find_one({"_id": ObjectId(id)})

    def update_product(self, db: Collection, id: str, product_id: int, obj_in: dict):
        db.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"products.$[elem]": obj_in}},
            array_filters=[{"elem.product_id": product_id}]
        )
        return db.find_one({"_id": ObjectId(id)})
    
    def remove_product(self, db: Collection, id: str, product_id: int):
        db.update_one({"_id": ObjectId(id)}, {"$pull": {"products": {"product_id": product_id}}})
        return db.find_one({"_id": ObjectId(id)})
    
    def remove_all_products(self, db: Collection, id: str):
        db.update_one({"_id": ObjectId(id)}, {"$set": {"products": []}})
        return db.find_one({"_id": ObjectId(id)})

crud = CartCRUD()