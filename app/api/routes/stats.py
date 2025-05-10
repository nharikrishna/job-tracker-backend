from fastapi import APIRouter

from app.dependencies.auth import CurrentUserDep
from app.dependencies.database import SessionDep
from app.services import stats as stats_service

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/")
def get_stats(db: SessionDep, user: CurrentUserDep):
    return stats_service.get_user_stats(db, user.id)
