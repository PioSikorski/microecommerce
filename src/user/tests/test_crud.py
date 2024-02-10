from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from src.tests.utils import random_email, random_lower_string
from src.user.app.api import crud
from src.user.app.api.model import UserCreate, UserUpdate
from src.core.security import verify_password

def test_create_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db=session, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db=session, obj_in=user_in)
    authenticated_user = crud.user.authenticate(session, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = crud.user.authenticate(db=session, email=email, password=password)
    assert user is None


def test_check_if_user_is_superuser(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.user.create(db=session, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user(session: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db=session, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False


def test_get_user(session: Session) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user = crud.user.create(db=session, obj_in=user_in)
    user_get = crud.user.get(db=session, id=user.id)
    assert user_get
    assert user.email == user_get.email
    assert jsonable_encoder(user) == jsonable_encoder(user_get)


def test_update_user(session: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.user.create(db=session, obj_in=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    crud.user.update(db=session, db_obj=user, obj_in=user_in_update)
    user_get = crud.user.get(db=session, id=user.id)
    assert user_get
    assert user.email == user_get.email
    assert verify_password(new_password, user_get.hashed_password)