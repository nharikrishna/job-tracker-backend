from uuid import UUID
from app.dependencies.database import SessionDep
from app.repositories import job_application_repo


def get_user_stats(db: SessionDep, user_id: UUID) -> dict:
    total = job_application_repo.get_total_applications(db, user_id)
    status_breakdown = job_application_repo.get_status_breakdown(db, user_id)
    role_breakdown = job_application_repo.get_role_breakdown(db, user_id)
    monthly_trend = job_application_repo.get_monthly_trend(db, user_id)

    return {
        "total_applications": total,
        "status_breakdown": status_breakdown,
        "role_breakdown": role_breakdown,
        "monthly_trend": monthly_trend,
    }
