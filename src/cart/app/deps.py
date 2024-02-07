from typing import Annotated

from pymongo import MongoClient
from pymongo.database import Database
from fastapi import Depends
from contextlib import contextmanager
from typing import Generator, Any


MONGODB_URL = "mongodb://myuser:mysecretpassword@mongodb:27017/"

client = MongoClient(MONGODB_URL)

db = client["orderdb"]

@contextmanager
def get_db() -> Generator[Any, Any, Any]:
    try:
        yield db.collection
    finally:
        client.close()

SessionDep = Annotated[Database, Depends(get_db)]