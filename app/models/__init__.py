from sqlmodel import SQLModel

from .job_application_model import JobApplication
from .resume_model import ResumeMatch
from .user_model import User


def get_metadata():
    return SQLModel.metadata
