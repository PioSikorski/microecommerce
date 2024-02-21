from typing import Dict

from fastapi.testclient import TestClient
from sqlmodel import Session

from src.user.app.api.model import User
from src.user.app.api.schema import UserCreate, UserUpdate
from src.user.app.api.crud import crud
from src.tests.utils import random_email, random_lower_string
from src.core.config import settings


def user_authentication_headers(client: TestClient, email: str, password: str) -> Dict[str, str]:
    data = {"username": email, "password": password}
    response = client.post(f"/login/access-token", data=data)
    token = response.json()
    auth_token = token["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(session: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create(db=session, obj_in=user_in)
    return user


def authentication_token_from_email(client: TestClient, email: str, session: Session) -> Dict[str, str]:
    password = random_lower_string()
    user = crud.get_by_email(db=session, email=email)
    if not user:
        user_in = UserCreate(email=email, password=password)
        user = crud.create(db=session, obj_in=user_in)
    else:
        user_in = UserUpdate(password=password)
        user = crud.update(db=session, db_obj=user, obj_in=user_in)
    return user_authentication_headers(client=client, email=email, password=password)


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post("/login/access-token", data=login_data)
    tokens = response.json()
    token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers