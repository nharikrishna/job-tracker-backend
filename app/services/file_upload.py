import os
import shutil
from typing import cast
from uuid import UUID

from fastapi import UploadFile

from app.core.config import get_settings
from app.services import constants
from app.utils.enums import FileTypeEnum

settings = get_settings()


def save_file(file: UploadFile, file_type: FileTypeEnum, job_id: UUID) -> str:
    if settings.app_env != constants.DEV:
        raise NotImplementedError("File storage not supported in this environment yet.")

    folder = constants.RESUMES
    if file_type == FileTypeEnum.JOB_DESCRIPTION:
        folder = constants.JOB_DESCRIPTIONS

    filename = f"{job_id}_{file.filename}"
    path = os.path.join(constants.MEDIA, folder, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return cast(str, path)
