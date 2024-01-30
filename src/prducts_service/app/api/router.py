from fastapi import APIRouter, HTTPException
from typing import Any
from sqlmodel import select

from api.model import ProductCreate, ProductUpdate, Product, ProductOut
from deps import SessionDep

router = APIRouter()


@router.get('/products', response_model=list[ProductOut])
def read_products(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    statement = select(Product).offset(skip).limit(limit)
    return session.exec(statement).all()


@router.get('/products/{id}', response_model=ProductOut)
def read_product(session: SessionDep, id: int) -> Any:
    product = session.get(Product, id)
    # products = session.get(list[Product], ids)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post('/products', response_model=ProductOut)
def create_product(*, session: SessionDep, product_in: ProductCreate) -> Any:
    product = Product.model_validate(product_in)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.put('/products/{id}', response_model=ProductOut)
def update_product(session: SessionDep, id: int, product_in: ProductUpdate) -> Any:
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    update_dict = product_in.dict(exclude_unset=True)
    product.model_validate(update_dict)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete('/products/{id}', response_model=ProductOut)
def delete_product(session: SessionDep, id: int) -> Any:
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return product