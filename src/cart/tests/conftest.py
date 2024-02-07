import pytest
from mongomock import MongoClient, Collection
from fastapi.testclient import TestClient

from src.core.security import create_access_token
from src.cart.app.deps import get_db
from src.cart.app.main import app


@pytest.fixture(name="db")
def mock_db():
    client = MongoClient()
    db = client.db
    collection = db.collection
    yield collection
    client.close()
    
@pytest.fixture(name="client")  
def client_fixture(db: Collection):  
    def get_db_override():  
        return db

    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()