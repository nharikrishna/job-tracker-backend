from typing import List
from uuid import UUID

from fastapi import HTTPException, status

from app.dependencies.database import SessionDep
from app.models import JobApplication
from app.repositories import job_application_repo as repo
from app.schemas import job_application_schema as schema
from app.utils.constants import errorcodes


def create_job(job_data: schema.JobBase, user_id: UUID, db: SessionDep) -> JobApplication:
    job = JobApplication(
        user_id=user_id,
        company=job_data.company,
        role=job_data.role,
        status=job_data.status,
        applied_date=job_data.applied_date,
        notes=job_data.notes,
        tags=job_data.tags,
        resume_file_path=job_data.resume_file_path,
        job_description_file_path=job_data.job_description_file_path,
    )
    return repo.create_job_application(job, db)


def get_jobs(user_id: UUID, db: SessionDep) -> List[JobApplication]:
    return repo.get_jobs_by_user(user_id, db)


def get_job_by_id(job_id: UUID, user_id: UUID, db: SessionDep) -> JobApplication:
    job = repo.get_job_by_id(job_id, db)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errorcodes.JOB_NOT_FOUND)
    if job.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errorcodes.UNAUTHORIZED)
    return job


def update_job(job_id: UUID, update: schema.JobUpdate, user_id: UUID, db: SessionDep) -> JobApplication:
    job = repo.get_job_by_id(job_id, db)
    if not job:
        raise HTTPException(status_code=404, detail=errorcodes.JOB_NOT_FOUND)
    if job.user_id != user_id:
        raise HTTPException(status_code=403, detail=errorcodes.UNAUTHORIZED)

    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(job, field, value)

    return repo.create_job_application(job, db)


def delete_job(job_id: UUID, user_id: UUID, db: SessionDep) -> None:
    job = repo.get_job_by_id(job_id, db)
    if not job:
        raise HTTPException(status_code=404, detail=errorcodes.JOB_NOT_FOUND)
    if job.user_id != user_id:
        raise HTTPException(status_code=403, detail=errorcodes.UNAUTHORIZED)
    repo.delete_job_by_id(job, db)
