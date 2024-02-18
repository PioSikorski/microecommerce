from typing import Union, Set

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel, AutoString, ARRAY, String


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)
    is_superuser: bool = False
    full_name: Union[str, None] = None
    

class UserWithOrders(UserBase):
    orders_ids: Set[str]
    

class UserWithOrdersOut(UserBase):
    id: int
    orders_ids: Set[str]
    

class UserCreate(UserBase):
    password: str
    
    
class UserCreateOpen(SQLModel):
    email: EmailStr
    password: str
    full_name: Union[str, None] = None
    

class UserUpdate(UserBase):
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None
    orders_ids: Union[Set[str], None] = None
    

class UserUpdateMe(BaseModel):
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None
    full_name: Union[str, None] = None
    
    
class User(UserBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    hashed_password: str
    orders_ids: Union[Set[str], None] = Field(sa_type=ARRAY(String()), default=None)


class UserOut(UserBase):
    id: int
 

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: Union[int, None] = None
    superuser: bool = False