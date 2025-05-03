from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.utils.enums import JobStatusEnum


class JobBase(BaseModel):
    company: str
    role: str
    status: JobStatusEnum = JobStatusEnum.APPLIED
    applied_date: Optional[datetime] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    resume_file_path: str
    job_description_file_path: str


class JobCreate(JobBase):
    user_id: UUID


class JobOut(JobBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
