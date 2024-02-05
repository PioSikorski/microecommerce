from typing import Any, Dict, Optional, Union, List
from sqlmodel import Session, select


from src.core.sql_crud import CRUDBase
from src.product.app.api.model import Product
from src.product.app.api.schema import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Product]:
        return db.exec(select(Product).where(Product.name == name)).first()

    def get_category(self, db: Session, *, category: str, skip: int = 0, limit: int = 100) -> Optional[List[Product]]:
        return db.exec(select(Product).where(Product.category == category).offset(skip).limit(limit)).all()
    
    def create(self, db: Session, *, obj_in: ProductCreate) -> Product:
        db_obj = Product(
            name=obj_in.name,
            description=obj_in.description,
            category=obj_in.category,
            price=obj_in.price,
            quantity=obj_in.quantity,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Product, obj_in: Union[ProductUpdate, Dict[str, Any]]) -> Product:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def delete(self, db: Session, *, id: int):
        return super().remove(db, id=id)
        

product = CRUDProduct(Product)