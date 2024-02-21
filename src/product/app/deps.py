import os
from typing import Generator, Annotated

from sqlalchemy import create_engine
from sqlmodel import Session
from fastapi import Depends

from src.product.app.api.model import SQLModel
from src.core.config import PRODUCTDB_URL


engine = create_engine(PRODUCTDB_URL)

def get_db() -> Generator:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session     
    

SessionDep = Annotated[Session, Depends(get_db)]