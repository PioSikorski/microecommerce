from typing import Any, List

from fastapi import APIRouter, HTTPException, Depends
import requests

from src.order.app.deps import SessionDep
from src.core.consts import ORDER_STATUS
from src.order.app.api.crud import crud
from src.order.app.api.model import OrderCollection, OrderCreate, OrderUpdate, OrderOut


router = APIRouter(prefix='/orders',
                   tags=['orders'])


@router.get('/', response_model=OrderCollection)
def read_orders(session: SessionDep) -> Any:
    orders = crud.get_collection(db=session)
    return {"orders": orders}


@router.get('/{id}', response_model=OrderOut)
def read_user_orders(session: SessionDep, id: str) -> Any:
    order = crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get('/{id}/products', response_model=List)
def read_order_products(session: SessionDep, id: str) -> Any:
    order = crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    products = requests.get(f"http://localhost:8000/carts/{order.get('shoppingcart_id')}/products")
    return products.json()


@router.get('/status/{status}', response_model=List[OrderOut])
def read_order_by_status(session: SessionDep, status: str) -> Any:
    if status not in ORDER_STATUS:
        raise HTTPException(status_code=400, detail="Invalid status")
    return crud.get_all_by_status(db=session, status=status)
    

@router.post('/', response_model=OrderOut)
def create_order(*, session: SessionDep, order_in: OrderCreate) -> Any:
    data_in = OrderCreate.model_dump(order_in)
    order = crud.create(db=session, obj_in=data_in)
    return order
    

@router.put('/{id}', response_model=OrderOut)
def update_order(session: SessionDep, id: str, order_in: OrderUpdate) -> Any:
    order = crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    data_in = order_in.model_dump(exclude_unset=True)
    updated_order = crud.update(db=session, id=id, obj_in=data_in)
    return updated_order


@router.delete('/{id}', response_model=bool)
def delete_order(session: SessionDep, id: str) -> Any:
    order = crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return crud.delete(db=session, id=id)