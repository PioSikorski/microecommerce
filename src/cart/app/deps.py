from typing import Annotated, Generator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from fastapi import Depends

from src.core.config import CARTDB_URL, CART_MONGODB_DB


client = AsyncIOMotorClient(CARTDB_URL)
db = client[CART_MONGODB_DB]

def get_db() -> Generator:
    try:
        yield db.collection['carts']
    finally:
        pass

SessionDep = Annotated[AsyncIOMotorCollection, Depends(get_db)]