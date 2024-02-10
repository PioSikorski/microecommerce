from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from src.user.app.api.model import SQLModel
from src.user.app.main import app
from src.user.app.deps import get_db
from src.user.app.init_db import init_db
from src.core.config import settings
from src.tests.utils import get_superuser_token_headers
from src.user.tests.user import authentication_token_from_email


@pytest.fixture(name="session", scope="module")  
def session_fixture():  
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    init_db(Session(engine))
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client", scope="module")  
def client_fixture(session: Session):  
    def get_db_override():  
        return session

    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
    
    
@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, session: Session) -> Dict[str, str]:
    return authentication_token_from_email(client=client, email=settings.EMAIL_TEST_USER, session=session)