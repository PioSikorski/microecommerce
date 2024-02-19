from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.user.app.api.model import SQLModel
from src.user.app.main import app
from src.user.app.deps import engine
from src.user.app.init_db import init_db
from src.core.config import settings
from src.tests.utils import get_superuser_token_headers
from src.user.tests.user import authentication_token_from_email


@pytest.fixture(name="session", scope="module")
def db() -> Generator:
    with Session(engine) as session:
        SQLModel.metadata.create_all(engine)
        init_db(session)
        yield session
        SQLModel.metadata.clear(engine)
        init_db(session)


@pytest.fixture(name="client", scope="module")  
def client_fixture() -> Generator:  
    with TestClient(app) as c:
        yield c
    
    
@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, session: Session) -> Dict[str, str]:
    return authentication_token_from_email(client=client, email=settings.EMAIL_TEST_USER, session=session)