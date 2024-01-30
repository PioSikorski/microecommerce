from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class ProductCreate(ProductBase):
    name: str
    description: str
    price: float
    quantity: int
    

class ProductUpdate(ProductBase):
    pass


class ProductInDBBase(ProductBase):
    id: int
    


class Product(ProductInDBBase):
    pass


class ProductInDB(ProductInDBBase):
    pass