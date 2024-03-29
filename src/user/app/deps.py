import os
from typing import Generator, Annotated

from sqlmodel import Session, create_engine
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from src.user.app.api.model import User, TokenPayload, SQLModel
from src.core.config import USERDB_URL, settings
from src.user.app.init_db import init_db


engine = create_engine(USERDB_URL)

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl='/login/access-token')


def get_db() -> Generator:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        init_db(session)
        yield session
        
SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials',
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="User doesn't have enough privileges")
    return current_user