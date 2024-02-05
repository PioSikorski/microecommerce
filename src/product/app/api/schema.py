from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass
    

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class ProductInDBBase(ProductBase):
    id: int
    

class Product(ProductInDBBase):
    pass


class ProductInDB(ProductInDBBase):
    pass