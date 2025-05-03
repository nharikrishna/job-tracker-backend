from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.db.database import get_db

SessionDep = Annotated[Session, Depends(get_db)]
