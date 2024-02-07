from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from src.cart.app.deps import SessionDep
from src.cart.app.api.crud import crud
from src.core.security import verify_token
from src.cart.app.api.model import ShoppingCart, ShoppingCartOut, ShoppingCartCollection, ShoppingCartProduct, ShoppingCartCreate, ShoppingCartUpdate, ShoppingCartProductUpdate


router = APIRouter(prefix='/carts',
                   tags=['carts'])


@router.get('/', response_model=ShoppingCartCollection)
def read_carts(session: SessionDep) -> Any:
    carts = crud.get_collection(db=session)
    return {"shoppingCarts": carts}


@router.get('/{id}', response_model=ShoppingCartOut)
def read_cart(session: SessionDep, id: str) -> Any:
    cart = crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.get('/{id}/products', response_model=List[ShoppingCartProduct])
def read_cart_products(session: SessionDep, id: str) -> Any:
    cart = crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart.get("products", [])


@router.post('/', response_model=ShoppingCartOut)
def create_cart(*, session: SessionDep, cart_in: ShoppingCartCreate) -> Any:
    data_in = ShoppingCart(**cart_in)
    cart = crud.create(db=session, obj_in=data_in)
    return cart


@router.put('/{id}', response_model=ShoppingCartOut)
def update_cart(session: SessionDep, id: str, cart_in: ShoppingCartUpdate) -> Any:
    cart = crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    data_in = ShoppingCart(**cart_in)
    updated_cart = crud.update(db=session, id=id, obj_in=data_in)
    return updated_cart


@router.put('/{id}/add', response_model=ShoppingCartOut)
def add_product_to_cart(session: SessionDep, id: str, product_in: ShoppingCartProductUpdate) -> Any:
    cart = crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    updated_cart = crud.add_product(db=session, id=id, obj_in=product_in)
    return updated_cart


@router.put('/{order_id}/products/{product_id}', response_model=ShoppingCartOut)
def update_product_in_cart(session: SessionDep, cart_id: str, product_id: int, product_in: ShoppingCartProductUpdate) -> Any:
    cart = crud.get(db=session, id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    data_in = ShoppingCartProduct(**product_in)
    updated_cart = crud.update_product(db=session, id=cart_id, product_id=product_id, obj_in=data_in)
    return updated_cart


@router.delete('/{id}', response_model=ShoppingCartOut)
def delete_cart(session: SessionDep, id: str) -> Any:
    cart = crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    crud.delete(db=session, id=id)
    return cart


@router.delete('/{order_id}/products/{product_id}', response_model=ShoppingCartOut)
def delete_product_from_cart(session: SessionDep, cart_id: str, product_id: int) -> Any:
    cart = crud.get(db=session, id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    updated_cart = crud.remove_product(db=session, id=cart_id, product_id=product_id)
    return updated_cart


@router.delete('/{id}/products', response_model=ShoppingCartOut)
def delete_all_product(session: SessionDep, id: str) -> Any:
    cart = crud.get(db=session, id=id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    updated_cart = crud.remove_all_products(db=session, id=id)
    return updated_cart