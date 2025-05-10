from uuid import UUID

from fastapi import APIRouter, UploadFile, Form, File

from app.dependencies.auth import CurrentUserDep
from app.dependencies.database import SessionDep
from app.schemas.resume_schema import ResumeMatchOut, ResumeMatchCheck
from app.services import resume_match as service

router = APIRouter(prefix="/resume-match", tags=["resume match"])


@router.post("/check", response_model=ResumeMatchOut)
def check_resume_match(
        db: SessionDep,
        _: CurrentUserDep,
        job_id: UUID = Form(...),
        resume: UploadFile = File(...),
        job_description: UploadFile = File(...)
):
    resume_data = ResumeMatchCheck(
        job_id=job_id,
        resume=resume,
        job_description=job_description
    )
    return service.process_resume_match(resume_data, db)


@router.get("/{job_id}", response_model=ResumeMatchOut)
def get_resume_match_by_job_id(job_id: UUID, db: SessionDep, _: CurrentUserDep):
    return service.get_resume_match_by_job_id(job_id, db)
