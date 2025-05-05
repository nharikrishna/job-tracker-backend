from fastapi import FastAPI

from app.api.routes import auth
from app.api.routes import job_application
from app.api.routes import users
from app.api.routes import resume_match
from app.api.routes import stats
from app.core.config import get_settings

settings = get_settings()
app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(job_application.router)
app.include_router(resume_match.router)
app.include_router(stats.router)

@app.get("/ping")
def ping():
    return {"ping": "pong"}
