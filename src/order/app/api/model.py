from typing import Optional, Annotated, List

from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator


PyObjectId = Annotated[str, BeforeValidator(str)]


class Order(BaseModel):
    user_id: int
    status: str
    shoppingcart_id: str
    address: str
    phone: str


class OrderUpdate(Order):
    user_id: int = None
    status: Optional[str] = None
    shoppingcart_id: str = None
    address: Optional[str] = None
    phone: Optional[str] = None
  

class OrderCreate(Order):
    user_id: Optional[int] = None
    status: str = "pending"
    
    
class OrderOut(Order):
    id: PyObjectId = Field(alias="_id")
    
    
class OrderCollection(BaseModel):
    orders: List[Order]