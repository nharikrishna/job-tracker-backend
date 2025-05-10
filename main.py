from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.api.routes import auth
from app.api.routes import job_application
from app.api.routes import resume_match
from app.api.routes import stats
from app.api.routes import users
from app.core.config import get_settings
from app.utils.constants.constants import DEV

settings = get_settings()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(job_application.router)
app.include_router(resume_match.router)
app.include_router(stats.router)

if settings.app_env == DEV:
    app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/ping")
def ping():
    return {"ping": "pong"}
