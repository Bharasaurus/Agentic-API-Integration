import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, HttpUrl

class Settings(BaseSettings):
    PET_SERVICE_BASE_URL: HttpUrl = Field(..., env="PET_SERVICE_BASE_URL")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = Path(__file__).parent / ".env"
        env_file_encoding = "utf-8"

settings = Settings()