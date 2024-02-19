from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from src.core.sql_crud import CRUDBase
from src.product.app.api.model import Product
from src.product.app.api.schema import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Product]:
        return db.query(Product).filter(Product.name == name).first()

    def get_category(self, db: Session, *, category: str, skip: int = 0, limit: int = 100) -> Optional[List[Product]]:
        return db.query(Product).filter(Product.category == category).offset(skip).limit(limit).all()

    def update(
        self, db: Session, *, db_obj: Product, obj_in: Union[ProductUpdate, Dict[str, Any]]) -> Product:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def remove(self, db: Session, *, id: int):
        return super().delete(db, id=id)
        

crud = CRUDProduct(Product)