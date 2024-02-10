from typing import Any, Union

from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

from src.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
       
class CredentialsException(Exception):
    def __init__(self):
        super().__init__("Invalid authentication credentials")
        self.status_code = 401
        self.headers = {"WWW-Authenticate": "Bearer"}
        
credentials_exception = CredentialsException()
     
        
def verify_token(token: dict) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user = {"user_id": int(payload.get("sub")), "superuser": payload.get("superuser")}
        if user["user_id"] is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


def create_access_token(subject: Union[int, Any], superuser: Union[bool, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "superuser": str(superuser), "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)