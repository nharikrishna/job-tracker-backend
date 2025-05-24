import os
import uuid
import shutil
from typing import cast
from uuid import UUID

from fastapi import UploadFile

from app.core.config import get_settings
from app.services import constants
from app.utils.constants.constants import DEV
from app.utils.enums import FileTypeEnum

settings = get_settings()

if settings.app_env != DEV:
    from app.external.supabase_client import supabase


def save_file(file: UploadFile, file_type: FileTypeEnum, job_id: UUID) -> str:
    folder = constants.RESUMES
    if file_type == FileTypeEnum.JOB_DESCRIPTION:
        folder = constants.JOB_DESCRIPTIONS

    filename = f"{job_id}_{uuid.uuid4()}_{file.filename}"

    if settings.app_env == DEV:
        path = os.path.join(constants.MEDIA, folder, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return cast(str, path)

    else:
        storage_path = f"{folder}/{filename}"
        contents = file.file.read()
        res = supabase.storage.from_(settings.supabase_bucket).upload(
            path=storage_path,
            file=contents,
            file_options={"content-type": file.content_type}
        )

        if res.error:
            raise RuntimeError(f"Upload failed: {res.error.message}")

        return supabase.storage.from_(settings.supabase_bucket).get_public_url(storage_path)
