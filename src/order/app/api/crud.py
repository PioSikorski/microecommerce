from typing import List

from pymongo.collection import Collection

from src.core.nosql_crud import BaseCRUD


class OrderCRUD(BaseCRUD):
    async def get_all_by_status(self, db: Collection, status: str) -> List:
        orders = []
        async for order in db.find({"status": status}):
            orders.append(order)
        return orders
    
    async def get_all_by_user(self, db: Collection, user_id: int) -> List:
        orders = []
        async for order in db.find({"user_id": user_id}):
            orders.append(order)
        return orders

crud = OrderCRUD()