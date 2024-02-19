from typing import Any, List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from src.cart.app.deps import SessionDep
from src.cart.app.api.crud import crud
from src.core.security import verify_token
from src.cart.app.api.model import ShoppingCartOut, ShoppingCartProduct, ShoppingCartCreate, ShoppingCartUpdate, ShoppingCartProductUpdate
from src.cart.app.api.utils import calculate_total


router = APIRouter(prefix='/carts',
                   tags=['carts'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login/access-token')


@router.get('/', response_model=List[ShoppingCartOut])
async def read_carts(session: SessionDep, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    if user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    carts = await crud.get_all(db=session)
    return carts
    
    
@router.get('/{id}', response_model=ShoppingCartOut)
async def read_cart(session: SessionDep, id: str, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    cart = await crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    if cart.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return cart


@router.get('/{id}/products', response_model=List[ShoppingCartProduct])
async def read_cart_products(session: SessionDep, id: str, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    cart = await crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    if cart.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return cart.get("products", [])


@router.post('/', response_model=ShoppingCartOut)
async def create_cart(*, session: SessionDep, cart_in: ShoppingCartCreate, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    cart_in.user_id = user.get("user_id")
    cart_in.total_amount = calculate_total(cart_in)
    data_in = cart_in.model_dump()
    cart = await crud.create(db=session, obj_in=data_in)
    if cart.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return cart


@router.put('/{id}', response_model=ShoppingCartOut)
async def update_cart(session: SessionDep, id: str, cart_in: ShoppingCartUpdate, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    cart = await crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    if cart.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    data_in = cart_in.model_dump(exclude_unset=True)
    updated_cart = await crud.update(db=session, id=id, obj_in=data_in)
    return updated_cart


@router.put('/{id}/add', response_model=ShoppingCartOut)
async def add_product_to_cart(session: SessionDep, id: str, product_in: ShoppingCartProductUpdate, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    cart = await crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    if cart.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    data_in = product_in.model_dump(exclude_unset=True)
    return await crud.add_product(db=session, id=id, obj_in=data_in)


@router.put('/{cart_id}/products/{product_id}', response_model=ShoppingCartOut)
async def update_product_in_cart(session: SessionDep, cart_id: str, product_id: int, product_in: ShoppingCartProductUpdate, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    cart = await crud.get(db=session, id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    if cart.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    data_in = product_in.model_dump(exclude_unset=True)
    return await crud.update_product(db=session, id=cart_id, product_id=product_id, obj_in=data_in)


@router.delete('/{id}', response_model=ShoppingCartOut)
async def delete_cart(session: SessionDep, id: str, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    cart = await crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    if cart.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await crud.remove(db=session, id=id)


@router.delete('/{order_id}/products/{product_id}', response_model=ShoppingCartOut)
async def delete_product_from_cart(session: SessionDep, cart_id: str, product_id: int, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    cart = await crud.get(db=session, id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    if cart.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await crud.remove_product(db=session, id=cart_id, product_id=product_id)


@router.delete('/{id}/products', response_model=ShoppingCartOut)
async def delete_all_product(session: SessionDep, id: str, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    cart = await crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    if cart.get("user_id") != user.get("user_id") and user.get("superuser") == "False":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await crud.remove_all_products(db=session, id=id)