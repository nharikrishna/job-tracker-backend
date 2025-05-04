from fastapi import FastAPI

from app.api.routes import auth
from app.api.routes import users
from app.core.config import get_settings

settings = get_settings()
app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/ping")
def ping():
    return {"ping": "pong"}
