from typing import Any, List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import requests

from src.core.security import verify_token
from src.order.app.deps import SessionDep
from src.core.consts import ORDER_STATUS
from src.order.app.api.crud import crud
from src.order.app.api.model import OrderCreate, OrderUpdate, OrderOut


router = APIRouter(prefix='/orders',
                   tags=['orders'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login/access-token')


@router.get('/', response_model=List[OrderOut])
async def read_orders(session: SessionDep, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    if user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    orders = await crud.get_all(db=session)
    return orders


@router.get('/{id}', response_model=OrderOut)
async def read_user_orders(session: SessionDep, id: str, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    order = await crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return order


@router.get('/{id}/products', response_model=List)
async def read_order_products(session: SessionDep, id: str, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)   
    order = await crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    cart_id = order.get("shoppingcart_id")
    products = await requests.get(f"http://cart_service:8003/carts/{cart_id}/products")
    return products.json()


@router.get('/status/{status}', response_model=List[OrderOut])
async def read_order_by_status(session: SessionDep, status: str, token: str = Depends(oauth2_scheme)) -> Any:
    if status not in ORDER_STATUS:
        raise HTTPException(status_code=400, detail="Invalid status")
    user = verify_token(token)
    if user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await crud.get_all_by_status(db=session, status=status)
    

@router.post('/', response_model=OrderOut)
async def create_order(*, session: SessionDep, order_in: OrderCreate, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    if order_in.user_id is None:
        user_id = user.get("user_id")
        order_in.user_id = user_id
    data_in = order_in.model_dump()
    order = await crud.create(db=session, obj_in=data_in)
    return order
    

@router.put('/{id}', response_model=OrderOut)
async def update_order(session: SessionDep, id: str, order_in: OrderUpdate, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    order = await crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    data_in = order_in.model_dump(exclude_unset=True)
    if 'status' in data_in and user.get("superuser") == "False":
        raise HTTPException(status_code=403, detail="Only superuser can change status")
    updated_order = await crud.update(db=session, id=id, obj_in=data_in)
    return updated_order


@router.delete('/{id}', response_model=OrderOut)
async def delete_order(session: SessionDep, id: str, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    order = await crud.get(db=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await crud.remove(db=session, id=id)