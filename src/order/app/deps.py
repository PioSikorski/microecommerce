import os
from typing import Annotated, Generator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from fastapi import Depends

from src.core.config import ORDERDB_URL, ORDER_MONGODB_DB


# MONGODB_USER = os.getenv("ORDER_MONGODB_USER")
# MONGODB_PASSWORD = os.getenv("ORDER_MONGODB_PASSWORD")
# MONGODB_HOST = os.getenv("ORDER_MONGODB_HOST")
# MONGODB_DB = os.getenv("ORDER_MONGODB_DB")

# DATABASE_URL = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}"

client = AsyncIOMotorClient(ORDERDB_URL)
db = client[ORDER_MONGODB_DB]

def get_db() -> Generator:
    try:
        yield db.collection['orders']
    finally:
        pass

SessionDep = Annotated[AsyncIOMotorCollection, Depends(get_db)]