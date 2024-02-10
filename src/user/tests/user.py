from typing import Dict

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.user.app.api.model import User
from src.user.app.api.schema import UserCreate, UserUpdate
from src.user.app.api import crud
from src.tests.utils import random_email, random_lower_string


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
    user = crud.user.create(db=session, obj_in=user_in)
    return user


def authentication_token_from_email(client: TestClient, email: str, session: Session) -> Dict[str, str]:
    password = random_lower_string()
    user = crud.user.get_by_email(db=session, email=email)
    if not user:
        user_in = UserCreate(email=email, password=password)
        user = crud.user.create(db=session, obj_in=user_in)
    else:
        user_in = UserUpdate(password=password)
        user = crud.user.update(db=session, obj_in=user_in)
    return user_authentication_headers(client=client, email=email, password=password)