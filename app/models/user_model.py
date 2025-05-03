from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field

from app.utils.enums import UserRoleEnum


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    role: UserRoleEnum = Field(default=UserRoleEnum.USER)
    name: str = Field(nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
