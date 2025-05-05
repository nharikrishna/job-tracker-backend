from fastapi import UploadFile, HTTPException

from app import models
from app.dependencies.database import SessionDep
from app.repositories import job_application_repo
from app.repositories import resume_match_repo as repo
from app.schemas import resume_schema as schema
from app.services import gemini
from app.services.constants import ALLOWED_EXTENSIONS
from app.services.file_upload import save_file
from app.utils.constants import errorcodes
from app.utils.enums import FileTypeEnum
from uuid import UUID


def validate_extension(file: UploadFile):
    if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Only {ALLOWED_EXTENSIONS}"
        )


def create_resume_match(resume_create: schema.ResumeMatchCreate, db: SessionDep):
    existing = repo.get_resume_match_by_job_id(resume_create.job_id, db)
    if existing:
        repo.delete_resume_match_by_job_id(resume_create.job_id, db)

    resume_match = models.ResumeMatch(**resume_create.model_dump())
    repo.create_resume_match(resume_match, db)
    return resume_match


def update_job_file_paths(job: models.JobApplication, db: SessionDep):
    job_application_repo.save_job_application(job, db)


def process_resume_match(resume_data: schema.ResumeMatchCheck, db: SessionDep):
    validate_extension(resume_data.resume)
    validate_extension(resume_data.job_description)

    job = job_application_repo.get_job_by_id(resume_data.job_id, db)
    if not job:
        raise HTTPException(status_code=404, detail=errorcodes.JOB_NOT_FOUND)

    resume_path = save_file(resume_data.resume, FileTypeEnum.RESUME, job.id)
    job_description_path = save_file(resume_data.job_description, FileTypeEnum.JOB_DESCRIPTION, job.id)

    score, suggestions = gemini.run_resume_matching(resume_data.resume.file, resume_data.job_description.file)

    resume_create = schema.ResumeMatchCreate(
        job_id=job.id,
        score=score,
        suggestion_keywords=suggestions,
    )
    resume_match = create_resume_match(resume_create, db)

    job.resume_file_path = resume_path
    job.job_description_file_path = job_description_path
    update_job_file_paths(job, db)

    return resume_match


def get_resume_match_by_job_id(job_id: UUID, db: SessionDep):
    match = repo.get_resume_match_by_job_id(job_id, db)
    if not match:
        raise HTTPException(status_code=404, detail=errorcodes.RESUME_MATCH_NOT_FOUND)
    return match
