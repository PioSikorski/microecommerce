import pytest
from mongomock import MongoClient, Collection
from fastapi.testclient import TestClient

from src.core.security import create_access_token
from src.order.app.deps import get_db
from src.order.app.main import app


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
    
@pytest.fixture(name="superuser_token_headers", scope="module")
def super_token_headers():
    payload = create_access_token(subject=1, superuser=True)
    return {"Authorization": f"Bearer {payload}"}
    
@pytest.fixture(name="normal_user_token_headers", scope="module")
def normal_user_token_headers():
    payload = create_access_token(subject=2, superuser=False)
    return {"Authorization": f"Bearer {payload}"}