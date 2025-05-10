from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

from app.utils.enums import JobStatusEnum

if TYPE_CHECKING:
    from app.models import ResumeMatch


class JobApplication(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")

    company: str
    role: str
    status: JobStatusEnum = Field(default=JobStatusEnum.APPLIED)

    application_date: Optional[datetime] = Field(default=None, nullable=True)
    notes: Optional[str] = Field(default=None, nullable=True)
    resume_file_path: Optional[str] = Field(default=None, nullable=True)
    job_description_file_path: Optional[str] = Field(default=None, nullable=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

    resume_match: Optional["ResumeMatch"] = Relationship(
        back_populates="job",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
