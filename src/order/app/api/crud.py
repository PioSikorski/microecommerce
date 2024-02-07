from pymongo.collection import Collection
from bson import ObjectId

from src.core.nosql_crud import BaseCRUD


class OrderCRUD(BaseCRUD):
    def get_all_by_status(self, db: Collection, status: str):
        return list(db.find({"status": status}))
    
    def get_all_by_user(self, db: Collection, user_id: str):
        return list(db.find({"user_id": user_id}))

crud = OrderCRUD()