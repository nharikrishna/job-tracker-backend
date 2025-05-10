from fastapi import APIRouter, status

from app.dependencies.auth import CurrentUserDep, AdminDep
from app.dependencies.database import SessionDep
from app.schemas.user_schema import *
from app.services import users as user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: SessionDep):
    return user_service.create_user(user, db)


@router.get("/me", response_model=UserRead)
def get_user(user: CurrentUserDep):
    return user


@router.patch("/me", response_model=UserRead)
def update_user(update: UserUpdate, db: SessionDep, user: CurrentUserDep):
    return user_service.update_user(user.id, update, db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: SessionDep, _: AdminDep):
    user_service.delete_user(user_id, db)
    return
