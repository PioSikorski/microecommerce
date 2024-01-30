from sqlalchemy import create_engine
from typing import Generator, Annotated
from sqlmodel import Session
from fastapi import Depends


DATABASE_URL = "postgresql://myuser:mysecretpassword@postgres:5432/productdb"

engine = create_engine(DATABASE_URL)

def get_db() -> Generator:
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_db)]