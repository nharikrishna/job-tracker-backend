from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError

from app.core.config import get_settings
from app.dependencies.database import SessionDep
from app.models import User
from app.utils.constants import errorcodes
from app.utils.enums import UserRoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
tokenDep = Annotated[str, Depends(oauth2_scheme)]

settings = get_settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm


def get_current_user(token: tokenDep, db: SessionDep) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("subject")
        if user_id is None:
            raise HTTPException(status_code=401, detail=errorcodes.INVALID_TOKEN)

        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail=errorcodes.USER_NOT_FOUND)
        return user
    except (DecodeError, ExpiredSignatureError):
        raise HTTPException(status_code=403, detail=errorcodes.TOKEN_DECODE_ERROR)


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRoleEnum.ADMIN.value:
        raise HTTPException(status_code=403, detail=errorcodes.ADMIN_ONLY)
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
AdminDep = Annotated[User, Depends(require_admin)]
