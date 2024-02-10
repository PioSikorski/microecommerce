from typing import Any, Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.user.app.api.model import UserOut, Token
from src.core.config import settings
from src.user.app.deps import SessionDep, CurrentUser
from src.core.security import create_access_token
from src.user.app.api import crud

router = APIRouter(tags=['login'])


@router.post("/login/access-token")
def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(db=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            subject=user.id, superuser=user.is_superuser, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=UserOut)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user