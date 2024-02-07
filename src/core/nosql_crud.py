from pymongo.collection import Collection
from bson.objectid import ObjectId


class BaseCRUD:
    def get(self, db: Collection, id: str):
        return db.find_one({"_id": ObjectId(id)})

    def create(self, db: Collection, obj_in: dict):
        id = db.insert_one(obj_in).inserted_id
        return db.find_one({"_id": id})
    
    def update(self, db: Collection, id: str, obj_in: dict):
        db.update_one({"_id": ObjectId(id)}, {"$set": obj_in})
        return db.find_one({"_id": ObjectId(id)})

    def delete(self, db: Collection, id: str):
        db.delete_one({"_id": ObjectId(id)})
        
    def get_collection(self, db: Collection):
        return list(db.find())