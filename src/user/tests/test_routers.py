from typing import Dict

from fastapi.testclient import TestClient
from sqlmodel import Session

from src.user.app.api.model import UserCreate
from src.core.config import settings
from src.tests.utils import random_email, random_lower_string
from src.user.app.api import crud


def test_get_users_superuser_me(client: TestClient, superuser_token_headers: Dict[str, str]) -> None:
    response = client.get("/users/me", headers=superuser_token_headers)
    current_user = response.json()
    assert current_user
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(client: TestClient, normal_user_token_headers: Dict[str, str]) -> None:
    response = client.get("/users/me", headers=normal_user_token_headers)
    current_user = response.json()
    assert current_user
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_email(client: TestClient, superuser_token_headers: dict, session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    response = client.post("/users/", headers=superuser_token_headers, json=data)
    assert 200 <= response.status_code < 300
    created_user = response.json()
    user = crud.user.get_by_email(db=session, email=email)
    assert user
    assert user.email == created_user["email"]


def test_get_existing_user(client: TestClient, superuser_token_headers: dict, session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db=session, obj_in=user_in)
    id = user.id
    response = client.get(f"/users/{id}", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    api_user = response.json()
    existing_user = crud.user.get_by_email(db=session, email=email)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_create_user_existing_username(client: TestClient, superuser_token_headers: dict, session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    crud.user.create(db=session, obj_in=user_in)
    data = {"email": email, "password": password}
    response = client.post("/users/", headers=superuser_token_headers, json=data)
    created_user = response.json()
    assert response.status_code == 400
    assert "id" not in created_user


def test_create_user_by_normal_user(client: TestClient, normal_user_token_headers: Dict[str, str]) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    response = client.post("/users/", headers=normal_user_token_headers, json=data)
    assert response.status_code == 400


def test_read_users(client: TestClient, superuser_token_headers: dict, session: Session) -> None:
    for i in range(2):
        email = random_email()
        password = random_lower_string()
        user_in = UserCreate(email=email, password=password)
        crud.user.create(db=session, obj_in=user_in)
    response = client.get("/users/", headers=superuser_token_headers)
    all_users = response.json()
    assert len(all_users) > 1
    for user in all_users:
        assert "email" in user
        
        
def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post("/login/access-token", data=login_data)
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
    

def test_use_access_token(client: TestClient, superuser_token_headers: Dict[str, str]) -> None:
    response = client.post("/login/test-token", headers=superuser_token_headers)
    result = response.json()
    assert response.status_code == 200
    assert "email" in result