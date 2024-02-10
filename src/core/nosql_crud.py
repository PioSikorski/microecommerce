from pymongo.collection import Collection
from bson.objectid import ObjectId


class BaseCRUD:
    def get(self, db: Collection, id: str) -> dict:
        return db.find_one({"_id": ObjectId(id)})

    def create(self, db: Collection, obj_in: dict) -> dict:
        id = db.insert_one(obj_in).inserted_id
        return db.find_one({"_id": id})
    
    def update(self, db: Collection, id: str, obj_in: dict) -> dict:
        db.update_one({"_id": ObjectId(id)}, {"$set": obj_in})
        return db.find_one({"_id": ObjectId(id)})

    def delete(self, db: Collection, id: str) -> bool:
        return (db.delete_one({"_id": ObjectId(id)})).acknowledged
        
    def get_collection(self, db: Collection) -> list:
        return list(db.find())