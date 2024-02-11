import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from src.product.app.api.model import SQLModel
from src.product.app.main import app
from src.product.app.deps import get_db
from src.core.security import create_access_token


@pytest.fixture(name="session")  
def session_fixture():  
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  


@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_db_override():  
        return session

    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
    
@pytest.fixture(name="superuser_token_headers", scope="module")
def super_token_headers():
    payload = create_access_token(subject=1, superuser=True)
    return {"Authorization" : f"Bearer {payload}"}
    
@pytest.fixture(name="normal_user_token_headers", scope="module")
def normal_user_token_headers():
    payload = create_access_token(subject=2, superuser=False)
    return {"Authorization" : f"Bearer {payload}"}