from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.utils.enums import JobStatusEnum


class JobBase(BaseModel):
    company: str
    role: str
    status: JobStatusEnum = JobStatusEnum.WISHLIST
    applied_date: Optional[datetime] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    resume_file_path: str
    job_description_file_path: str


class JobUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[JobStatusEnum] = None
    applied_date: Optional[datetime] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    resume_file_path: Optional[str] = None
    job_description_file_path: Optional[str] = None


class JobOut(JobBase):
    id: UUID
    user_id: UUID
    company: str
    role: str
    created_at: datetime
    updated_at: datetime
