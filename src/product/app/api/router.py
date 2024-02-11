from typing import Any, List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from src.core.security import verify_token

from src.product.app.api.model import Product, ProductOut
from src.product.app.api.schema import ProductCreate, ProductUpdate
from src.product.app.deps import SessionDep
from src.product.app.api import crud


router = APIRouter(prefix='/products',
                   tags=['products'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login/access-token')


@router.get('/', response_model=List[ProductOut])
def read_products(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    statement = select(Product).offset(skip).limit(limit)
    return session.exec(statement).all()


@router.get('/{name}', response_model=ProductOut)
def read_product_by_name(session: SessionDep, name: str) -> Any:
    product = crud.product.get_by_name(db=session, name=name)
    return product


@router.get('/{id}', response_model=ProductOut)
def read_product(session: SessionDep, id: int) -> Any:
    product = crud.product.get(db=session, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get('/category/{category}', response_model=List[ProductOut])
def read_category(session: SessionDep, category: str, skip: int = 0, limit: int = 100):
    products = crud.product.get_category(db=session, category=category)
    return products


@router.post('/', response_model=ProductOut)
def create_product(*, session: SessionDep, product_in: ProductCreate, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    superuser = user.get("superuser")
    if superuser == "False":
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    product = crud.product.create(db=session, obj_in=product_in)
    return product


@router.put('/{id}', response_model=ProductOut)
def update_product(session: SessionDep,  id: int, product_in: ProductUpdate, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    superuser = user.get("superuser")
    if superuser == "False":
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    product = crud.product.get(db=session, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    data_in = ProductUpdate.model_dump(product_in)
    updated_product = crud.product.update(db=session, db_obj=product, obj_in=data_in)
    return updated_product


@router.delete('/{id}', response_model=ProductOut)
def delete_product(session: SessionDep,  id: int, token: str = Depends(oauth2_scheme)) -> Any:
    user = verify_token(token)
    superuser = user.get("superuser")
    if superuser == "False":
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    product = crud.product.get(db=session, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = crud.product.delete(db=session, id=id)
    return product