from datetime import datetime
from typing import Union, List
from sqlmodel import SQLModel, Field, Relationship


class OrderBase(SQLModel):
    total_amount: float
    status: str
    address: str
    phone: str


class OrderCreate(OrderBase):
    total_amount: Union[float, None] = None
    status: Union[str, None] = 'pending'
    address: Union[str, None] = None
    phone: Union[str, None] = None


class OrderUpdate(OrderBase):
    total_amount: Union[float, None] = None
    status: Union[str, None] = None
    address: Union[str, None] = None
    phone: Union[str, None] = None
    

class Order(OrderBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    order_date: datetime = Field(default_factory=datetime.utcnow)
    products: List["OrderProduct"] = Relationship(back_populates="order")
    
    
class OrderProductBase(SQLModel):
    product_id: int
    quantity: int
    unit_price: float
    

class OrderProductCreate(OrderProductBase):
    pass


class OrderProductUpdate(OrderProductBase):
    product_id: Union[int, None] = None
    quantity: Union[int, None] = None
    unit_price: Union[float, None] = None
    

class OrderProduct(OrderProductBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    order_id: Union[int, None] = Field(default=None, foreign_key="order.id", nullable=False)
    order: Order = Relationship(back_populates="products")
    product_id: int
    quantity: int
    unit_price: float
    
    
class OrderProductOut(OrderProductBase):
    id: int
    

class OrderCreateWithProducts(SQLModel):
    order: OrderCreate
    products: List["OrderProductCreate"]


class OrderOut(OrderBase):
    id: int
    order_date: datetime
    products: List["OrderProduct"]