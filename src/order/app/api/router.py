from typing import Any, List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import requests

from src.core.security import verify_token
from src.order.app.deps import SessionDep
from src.core.consts import ORDER_STATUS
from src.order.app.api.crud import crud
from src.order.app.api.model import Order, OrderCollection, OrderCreate, OrderUpdate, OrderOut


router = APIRouter(prefix='/orders',
                   tags=['orders'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login/access-token')


@router.get('/', response_model=OrderCollection)
def read_orders(session: SessionDep, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    if user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    orders = crud.get_collection(db=session)
    return {"orders": orders}


@router.get('/{id}', response_model=OrderOut)
def read_user_orders(session: SessionDep, id: str, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    order = crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return order


@router.get('/{id}/products', response_model=List)
def read_order_products(session: SessionDep, id: str, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)   
    order = crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    products = requests.get(f"http://localhost:8003/carts/{order.get('shoppingcart_id')}/products")
    return products.json()


@router.get('/status/{status}', response_model=List[OrderOut])
def read_order_by_status(session: SessionDep, status: str, token: str = Depends(oauth2_scheme)) -> Any:
    if status not in ORDER_STATUS:
        raise HTTPException(status_code=400, detail="Invalid status")
    user = verify_token(token)
    if user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return crud.get_all_by_status(db=session, status=status)
    

@router.post('/', response_model=OrderOut)
def create_order(*, session: SessionDep, order_in: OrderCreate, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    user_id = user.get("user_id")
    order_in.user_id = user_id
    data_in = OrderCreate.model_dump(order_in)
    order = crud.create(db=session, obj_in=data_in)
    return order
    

@router.put('/{id}', response_model=OrderOut)
def update_order(session: SessionDep, id: str, order_in: OrderUpdate, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    order = crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    data_in = order_in.model_dump(exclude_unset=True)
    if 'status' in data_in and user.get("superuser") == "False":
        raise HTTPException(status_code=403, detail="Only superuser can change status")
    updated_order = crud.update(db=session, id=id, obj_in=data_in)
    return updated_order


@router.delete('/{id}', response_model=bool)
def delete_order(session: SessionDep, id: str, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    order = crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return crud.delete(db=session, id=id)