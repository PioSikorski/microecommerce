from sqlmodel import Session, select

from src.user.app.api.model import User, UserCreate
from src.core.config import settings
from src.user.app.api.crud import crud


def init_db(session: Session) -> None:
    user = session.exec(select(User).where(User.email == f"{settings.FIRST_SUPERUSER}")).first()
    if not user:
        user_in = UserCreate(
            email= settings.FIRST_SUPERUSER,
            password= settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.create(db=session, obj_in=user_in)