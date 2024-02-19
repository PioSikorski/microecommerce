from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.product.app.api.model import SQLModel
from src.product.app.main import app
from src.product.app.deps import engine
from src.core.security import create_access_token


@pytest.fixture(name="session", scope="module")
def db() -> Generator:
    with Session(engine) as session:
        SQLModel.metadata.create_all(engine)
        yield session
        SQLModel.metadata.clear(engine)

@pytest.fixture(name="client", scope="module")  
def client_fixture() -> Generator:  
    with TestClient(app) as c:
        yield c
    
@pytest.fixture(name="superuser_token_headers", scope="module")
def super_token_headers():
    payload = create_access_token(subject=1, superuser=True)
    return {"Authorization" : f"Bearer {payload}"}
    
@pytest.fixture(name="normal_user_token_headers", scope="module")
def normal_user_token_headers():
    payload = create_access_token(subject=2, superuser=False)
    return {"Authorization" : f"Bearer {payload}"}