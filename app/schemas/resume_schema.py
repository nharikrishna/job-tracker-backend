from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class ResumeMatchBase(BaseModel):
    score: float
    suggestion_keywords: Optional[List[str]] = None


class ResumeMatchCreate(ResumeMatchBase):
    job_id: UUID


class ResumeMatchOut(ResumeMatchBase):
    id: UUID
    job_id: UUID
    created_at: datetime
