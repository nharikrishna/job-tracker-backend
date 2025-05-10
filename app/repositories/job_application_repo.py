from typing import List, Optional
from uuid import UUID

from sqlalchemy import func, extract
from sqlmodel import select

from app.dependencies.database import SessionDep
from app.models import JobApplication


def save_job_application(job: JobApplication, db: SessionDep) -> JobApplication:
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


def get_total_applications(db: SessionDep, user_id: UUID) -> int:
    return db.query(JobApplication).filter(JobApplication.user_id == user_id).count()


def get_status_breakdown(db: SessionDep, user_id: UUID) -> dict[str, int]:
    result = (
        db.query(JobApplication.status, func.count())
        .filter(JobApplication.user_id == user_id)
        .group_by(JobApplication.status)
        .all()
    )
    return {status.name: count for status, count in result}


def get_role_breakdown(db: SessionDep, user_id: UUID) -> dict[str, int]:
    result = (
        db.query(JobApplication.role, func.count())
        .filter(JobApplication.user_id == user_id)
        .group_by(JobApplication.role)
        .all()
    )
    return {role: count for role, count in result}


def get_monthly_trend(db: SessionDep, user_id: UUID) -> dict[str, int]:
    result = (
        db.query(
            extract("year", JobApplication.created_at).label("year"),
            extract("month", JobApplication.created_at).label("month"),
            func.count()
        )
        .filter(JobApplication.user_id == user_id)
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )
    return {f"{int(year):04d}-{int(month):02d}": count for year, month, count in result}
