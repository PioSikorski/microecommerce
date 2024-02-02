from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class OrderBase(BaseModel):
    total_amount: float
    status: str
    address: str
    phone: str


class OrderCreate(OrderBase):
    total_amount: Optional[float] = None
    status: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class OrderUpdate(OrderBase):
    total_amount: Optional[float] = None
    status: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class OrderInDBBase(OrderBase):
    id: int
    order_date: datetime
    products: list["OrderProduct"]


class Order(OrderInDBBase):
    pass


class OrderInDB(OrderInDBBase):
    pass


class OrderProductBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class OrderProductCreate(OrderProductBase):
    pass


class OrderProductUpdate(OrderProductBase):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None


class OrderProductInDBBase(OrderProductBase):
    id: int


class OrderProduct(OrderProductInDBBase):
    pass


class OrderProductInDB(OrderProductInDBBase):
    pass


class OrderCreateWithProducts(BaseModel):
    order: OrderCreate
    Products: list[OrderProductCreate]