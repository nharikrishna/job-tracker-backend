from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.dependencies.database import SessionDep
from app.schemas.user_schema import UserBase
from app.services.users import authenticate_user
from app.core.logging_config import log

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(db: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_input = UserBase(email=form_data.username, password=form_data.password)
    token = authenticate_user(user_input, db)

    return {
        "access_token": token,
        "token_type": "bearer"
    }