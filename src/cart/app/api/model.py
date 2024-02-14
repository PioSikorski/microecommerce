from typing import Optional, Annotated, List

from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId


PyObjectId = Annotated[str, BeforeValidator(str)]


class ShoppingCartProduct(BaseModel):
    product_id: int
    quantity: int  
    unit_price: float 


class ShoppingCart(BaseModel):
    user_id: int
    total_amount: float
    products: List["ShoppingCartProduct"]
    

class ShoppingCartCreate(ShoppingCart):
    user_id: Optional[int] = None
    total_amount: Optional[float] = None


class ShoppingCartUpdate(ShoppingCart):
    total_amount: Optional[float] = None
    products: Optional[List["ShoppingCartProduct"]] = None


class ShoppingCartOut(ShoppingCart):
    id: PyObjectId = Field(..., alias="_id")


class ShoppingCartProductUpdate(ShoppingCartProduct):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None


class ShoppingCartProductCreate(ShoppingCartProduct):
    pass