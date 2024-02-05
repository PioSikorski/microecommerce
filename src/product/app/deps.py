from typing import Generator, Annotated

from sqlalchemy import create_engine
from sqlmodel import Session
from fastapi import Depends

from src.product.app.api.model import SQLModel


DATABASE_URL = "postgresql://myuser:mysecretpassword@postgres:5432/productdb"

engine = create_engine(DATABASE_URL)

def get_db() -> Generator:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session     
    

SessionDep = Annotated[Session, Depends(get_db)]