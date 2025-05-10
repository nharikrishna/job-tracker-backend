from fastapi import HTTPException
from sqlmodel import Session

from app.core.security import *
from app.dependencies.database import SessionDep
from app.models import User
from app.repositories import user_repo
from app.schemas.user_schema import *
from app.services.constants import *
from app.utils.constants import errorcodes


def create_user(user_data: UserCreate, db: SessionDep) -> User:
    if user_repo.get_user_by_email(str(user_data.email), db):
        raise HTTPException(status_code=400, detail=errorcodes.USER_ALREADY_EXISTS)

    hashed_password = get_password_hash(user_data.password)
    user = User(**user_data.model_dump(exclude={KEY_PASSWORD}),
                password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(user_id: UUID, update_data: UserUpdate, db: SessionDep) -> User:
    user = user_repo.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail=errorcodes.USER_NOT_FOUND)

    updates = update_data.model_dump(exclude_unset=True)

    if KEY_PASSWORD in updates:
        updates[KEY_PASSWORD] = get_password_hash(updates[KEY_PASSWORD])

    for key, value in updates.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(user_id: UUID, db: SessionDep):
    user = user_repo.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail=errorcodes.USER_NOT_FOUND)

    db.delete(user)
    db.commit()


def authenticate_user(user_data: UserBase, db: Session) -> str:
    user = user_repo.get_user_by_email(str(user_data.email), db)
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail=errorcodes.INVALID_EMAIL_OR_PASSWORD)

    token = create_access_token(subject=user.id)
    return token
