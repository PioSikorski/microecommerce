from typing import Annotated, Generator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from fastapi import Depends



MONGODB_URL = "mongodb://myuser:mysecretpassword@cart-mongodb-container:27017/"

client = AsyncIOMotorClient(MONGODB_URL)
db = client["orderdb"]

def get_db() -> Generator:
    try:
        yield db.collection['carts']
    finally:
        pass

SessionDep = Annotated[AsyncIOMotorCollection, Depends(get_db)]