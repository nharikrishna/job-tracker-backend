from sqlalchemy import create_engine
from sqlmodel import Session

import app.core.config as config

settings = config.get_settings()
engine = create_engine(settings.DB.url)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
