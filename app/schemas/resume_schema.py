from datetime import datetime
from typing import Optional, List
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel


class ResumeMatchCheck(BaseModel):
    job_id: UUID
    resume: UploadFile
    job_description: UploadFile


class ResumeMatchCreate(BaseModel):
    job_id: UUID
    score: float
    suggestion_keywords: Optional[List[str]] = None


class ResumeMatchOut(ResumeMatchCreate):
    id: UUID
    created_at: datetime
