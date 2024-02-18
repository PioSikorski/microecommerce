from typing import Any, List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import requests

from src.core.security import verify_token
from src.order.app.deps import SessionDep
from src.core.consts import ORDER_STATUS
from src.order.app.api.crud import crud
from src.order.app.api.model import OrderCreate, OrderUpdate, OrderOut
from src.order.app.api.service import orderproduct_rpc, orderuser_rpc


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
    response = requests.get(f"http://cart-container:8000/carts/{cart_id}/products", headers={"Authorization": f"Bearer {token}"})
    data = response.json()
    return data
    

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
    cart_id = data_in.get("shoppingcart_id")
    cart_response = requests.get(f"http://cart-container:8000/carts/{cart_id}/products", headers={"Authorization": f"Bearer {token}"})
    products_data = cart_response.json()
    response_product_rpc = orderproduct_rpc.call(products_data)
    if response_product_rpc.get("status") == "failed":
        raise HTTPException(status_code=400, detail=response_product_rpc.get("message"))
    order = await crud.create(db=session, obj_in=data_in)
    order_data = {"user_id": order.get("user_id"), "order_id": str(order.get("_id"))}
    response_user_rpc = orderuser_rpc.call(order_data)
    if response_user_rpc.get("status") == "failed":
        order_id = order.get("_id")
        await crud.remove(db=session, id=order_id)
        raise HTTPException(status_code=400, detail=response_user_rpc.get("message"))
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