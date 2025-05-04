import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.utils.enums import UserRoleEnum


class UserBase(BaseModel):
    email: EmailStr
    password: str
    role: Optional[UserRoleEnum] = UserRoleEnum.USER


class UserCreate(UserBase):
    name: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserRead(BaseModel):
    id: UUID
    name: str
    role: UserRoleEnum
    email: EmailStr
    created_at: datetime.datetime

    class Config:
        from_attributes = True
