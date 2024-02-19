import random
import string
from typing import Dict

from fastapi.testclient import TestClient

from src.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_float() -> float:
    return round(random.random(), 2)


def random_int() -> int:
    return random.randint(5, 1000)


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


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