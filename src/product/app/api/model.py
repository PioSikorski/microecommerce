from typing import Union

from sqlmodel import SQLModel, Field


class ProductBase(SQLModel):
    name: str
    description: str
    category: str
    price: float
    quantity: int
    

class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Union[str, None] = None
    description: Union[str, None] = None
    category: Union[str, None] = None
    price: Union[float, None] = None
    quantity: Union[int, None] = None
    

class Product(ProductBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    name: str
    description: str
    category: str
    price: float
    quantity: int
    
    
class ProductOut(ProductBase):
    id: int