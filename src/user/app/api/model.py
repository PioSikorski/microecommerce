from typing import Union
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel, AutoString


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)
    is_superuser: bool = False
    full_name: Union[str, None] = None
    
    
class UserCreate(UserBase):
    password: str
    
    
class UserCreateOpen(SQLModel):
    email: EmailStr
    password: str
    full_name: Union[str, None] = None
    

class UserUpdate(UserBase):
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None
    

class UserUpdateMe(BaseModel):
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None
    full_name: Union[str, None] = None
    
    
class User(UserBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    hashed_password: str


class UserOut(UserBase):
    id: int
 

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: Union[int, None] = None
    superuser: bool = False