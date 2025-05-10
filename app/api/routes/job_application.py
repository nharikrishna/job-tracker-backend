from typing import List
from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies.auth import CurrentUserDep
from app.dependencies.database import SessionDep
from app.schemas.job_application_schema import JobBase, JobUpdate, JobOut
from app.services import job_application as service

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/", response_model=JobOut)
def create_job(job: JobBase, db: SessionDep, user: CurrentUserDep):
    return service.create_job(job, user.id, db)


@router.get("/", response_model=List[JobOut])
def get_jobs(db: SessionDep, user: CurrentUserDep):
    return service.get_jobs(user.id, db)


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: UUID, db: SessionDep, user: CurrentUserDep):
    return service.get_job_by_id(job_id, user.id, db)


@router.patch("/{job_id}", response_model=JobOut)
def update_job(job_id: UUID, update: JobUpdate, db: SessionDep, user: CurrentUserDep):
    return service.update_job(job_id, update, user.id, db)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: UUID, db: SessionDep, user: CurrentUserDep):
    service.delete_job(job_id, user.id, db)
    return
