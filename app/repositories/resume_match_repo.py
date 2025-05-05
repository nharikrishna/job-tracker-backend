from uuid import UUID

from sqlmodel import select

from app.dependencies.database import SessionDep
from app.models import ResumeMatch


def create_resume_match(match: ResumeMatch, db: SessionDep) -> None:
    db.add(match)
    db.commit()
    db.refresh(match)


def get_resume_match_by_job_id(job_id: UUID, db: SessionDep) -> ResumeMatch | None:
    return db.exec(select(ResumeMatch).where(ResumeMatch.job_id == job_id)).first()


def delete_resume_match_by_job_id(job_id: UUID, db: SessionDep) -> None:
    match = get_resume_match_by_job_id(job_id, db)
    if match:
        db.delete(match)
        db.commit()
