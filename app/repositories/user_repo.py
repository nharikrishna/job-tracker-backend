from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from app.dependencies.database import SessionDep
from app.models import User


def get_user_by_email(email: str, db: SessionDep) -> Optional[User]:
    query = select(User).where(User.email == email)
    result = db.exec(query)
    return result.first()


def get_user_by_id(user_id: UUID, db: Session) -> User | None:
    return db.get(User, user_id)
