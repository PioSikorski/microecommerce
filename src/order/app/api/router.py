from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from deps import SessionDep
from const import ORDER_STATUS
from api.model import Order, OrderCreateWithProducts, OrderUpdate, OrderOut, OrderProduct, OrderProductOut, OrderProductUpdate

router = APIRouter(prefix='/orders',
                   tags=['orders'])


@router.get('', response_model=list[OrderOut])
def read_orders(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    statement = select(Order).offset(skip).limit(limit)
    return session.exec(statement).all()


@router.get('/{id}', response_model=OrderOut)
def read_order(session: SessionDep, id: int) -> Any:
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get('/{id}/products', response_model=list[OrderProductOut])
def read_order_products(session: SessionDep, id: int) -> Any:
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.products


@router.get('/orders/status/{status}', response_model=list[OrderOut])
def read_order_by_status(session: SessionDep, status: str, skip: int = 0, limit: int = 100) -> Any:
    if status not in ORDER_STATUS:
        raise HTTPException(status_code=404, detail="Wrong status")
    statement = select(Order).filter(Order.status == status).offset(skip).limit(limit)
    return session.exec(statement).all()


@router.post('', response_model=OrderOut)
def create_order(*, session: SessionDep, order_in: OrderCreateWithProducts) -> Any:
    order_data = order_in.order.dict()
    order = Order(**order_data)
    session.add(order)
    session.commit()
    session.refresh(order)
    for product_data in order_in.products:
        product = OrderProduct(**product_data.model_dump(), order_id=order.id)
        session.add(product)
    session.commit()
    return order


@router.put('/{id}', response_model=OrderOut)
def update_order(session: SessionDep, id: int, order_in: OrderUpdate) -> Any:
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status not in ORDER_STATUS:
        raise HTTPException(status_code=400, detail="Wrong status")
    update_dict = order_in.model_dump(exclude_unset=True)
    order.model_validate(update_dict)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.put('/{id}/add', response_model=OrderOut)
def add_product_to_order(session: SessionDep, id: int, order_in: OrderCreateWithProducts) -> Any:
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for product_data in order_in.products:
        product = OrderProduct(**product_data.model_dump(), order_id=order.id)
        session.add(product)
    session.commit()
    session.refresh(order)
    return order


@router.put('/{order_id}/products/{product_id}', response_model=OrderProduct)
def update_product_in_order(session: SessionDep, order_id: int, product_id: int, product_in: OrderProductUpdate) -> Any:
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    product = next((product for product in order.products if product.product_id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found in the order")
    update_dict = product_in.model_dump(exclude_unset=True)
    product.model_validate(update_dict)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
 

@router.delete('/{id}', response_model=OrderOut)
def delete_order(session: SessionDep, id: int) -> Any:
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(order)
    session.commit()
    return order


@router.delete('/{order_id}/products/{product_id}', response_model=OrderOut)
def delete_product_from_order(session: SessionDep, order_id: int, product_id: int) -> Any:
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    product = next((product for product in order.products if product.product_id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found in the order")
    session.delete(product)
    session.commit()
    session.refresh(order)
    return order


@router.delete('/{id}/products', response_model=OrderOut)
def delete_all_product(session: SessionDep, id: int) -> Any:
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(order.products)
    session.commit()
    session.refresh(order)
    return order
    