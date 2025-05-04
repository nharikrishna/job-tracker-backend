from typing import List, Optional
from uuid import UUID

from sqlmodel import select

from app.dependencies.database import SessionDep
from app.models import JobApplication


def create_job_application(job: JobApplication, db: SessionDep) -> JobApplication:
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_jobs_by_user(user_id: UUID, db: SessionDep) -> List[JobApplication]:
    statement = select(JobApplication).where(JobApplication.user_id == user_id)
    return db.exec(statement).all()


def get_job_by_id(job_id: UUID, db: SessionDep) -> Optional[JobApplication]:
    return db.get(JobApplication, job_id)


def delete_job_by_id(job: JobApplication, db: SessionDep) -> None:
    db.delete(job)
    db.commit()
