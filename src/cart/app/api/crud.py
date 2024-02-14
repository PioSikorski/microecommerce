from typing import Dict

from pymongo.collection import Collection
from bson.objectid import ObjectId

from src.core.nosql_crud import BaseCRUD


class CartCRUD(BaseCRUD):
    async def add_product(self, db: Collection, id: str, obj_in: Dict) -> Dict:
        await db.update_one({"_id": ObjectId(id)}, {"$push": {"products": obj_in}})
        return await db.find_one({"_id": ObjectId(id)})

    async def update_product(self, db: Collection, id: str, product_id: int, obj_in: Dict) -> Dict:
        db.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"products.$[elem]": obj_in}},
            array_filters=[{"elem.product_id": product_id}]
        )
        return await db.find_one({"_id": ObjectId(id)})
    
    async def remove_product(self, db: Collection, db_obj: Dict, product_id: int) -> Dict:
            db_obj["products"] = [product for product in db_obj["products"] if product["product_id"] != product_id]
            await db.update_one({"_id": db_obj["_id"]}, {"$set": db_obj})
            return await db.find_one({"_id": db_obj["_id"]})
    
    async def remove_all_products(self, db: Collection, id: str) -> Dict:
        await db.update_one({"_id": ObjectId(id)}, {"$set": {"products": []}})
        return await db.find_one({"_id": ObjectId(id)})

crud = CartCRUD()