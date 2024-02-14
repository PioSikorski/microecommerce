from typing import List, Dict

from pymongo.collection import Collection
from bson.objectid import ObjectId


class BaseCRUD:
    async def get(self, db: Collection, id: str) -> Dict:
        return await db.find_one({"_id": ObjectId(id)})
    
    async def get_all(self, db: Collection) -> List[Dict]:
        carts = []
        async for cart in db.find():
            carts.append(cart)
        return carts

    async def create(self, db: Collection, obj_in: Dict) -> Dict:
        craete_obj = await db.insert_one(obj_in)
        id = craete_obj.inserted_id
        return await db.find_one({"_id": id})
    
    async def update(self, db: Collection, id: str, obj_in: Dict) -> Dict:
        await db.update_one({"_id": ObjectId(id)}, {"$set": obj_in})
        return await db.find_one({"_id": ObjectId(id)})

    async def remove(self, db: Collection, id: str) -> Dict:
        deleted_object = await db.find_one_and_delete({"_id": ObjectId(id)})
        return deleted_object