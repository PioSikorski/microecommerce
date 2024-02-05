import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from src.product.app.api.model import SQLModel
from src.product.app.main import app
from src.product.app.deps import get_db


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