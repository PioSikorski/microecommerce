from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from src.user.app.api.model import User, UserCreateOpen, UserOut, UserUpdateMe
from src.user.app.api.schema import UserCreate
from src.user.app.deps import SessionDep, get_current_superuser, CurrentUser
from src.user.app.api import crud


router = APIRouter(prefix="/users",
                   tags=['users'])


@router.get("/", dependencies=[Depends(get_current_superuser)], response_model=List[UserOut])
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve list of users.
    """
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement)


@router.post("/", dependencies=[Depends(get_current_superuser)], response_model=UserOut)
def create_user(session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create user.
    """
    user = crud.user.get_by_email(db=session, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail='User already exists.')
    user = crud.user.create(db=session, obj_in=user_in)
    return user


@router.get('/me', response_model=UserOut)
def read_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user
    
    
@router.put('/me', response_model=UserOut)
def update_user_me(session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser) -> Any:
    """
    Update own user.
    """
    user_in = UserUpdateMe(**user_in)
    updated_user = crud.user.update(db=session, obj_in=user_in)
    return updated_user


@router.post('/create', response_model=UserOut)
def create_user_open(session: SessionDep, user_in: UserCreateOpen) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = crud.user.get_by_email(db=session, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail='User already exists.')
    user_create = crud.user.create(db=session, obj_in=user_in)
    return user_create


@router.get('/{id}', response_model=UserOut)
def read_user_by_id(id: int, session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db=session, id=id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return user