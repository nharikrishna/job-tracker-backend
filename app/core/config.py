from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseModel):
    DIALECT: str
    DRIVER: str
    USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: str
    NAME: str

    @property
    def url(self):
        return (
            f"{self.DIALECT}+{self.DRIVER}://{self.USERNAME}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.NAME}"
        )


class Settings(BaseSettings):
    app_env: str
    DB: DatabaseSettings
    secret_key: str
    algorithm: str
    access_token_expire: int

    gemini_api_key: str
    gemini_api_url: str

    supabase_url: str
    supabase_key: str
    supabase_bucket: str

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"
        env_nested_delimiter = "__"


@lru_cache
def get_settings():
    return Settings()
