import os
from functools import lru_cache
from pydantic import BaseSettings, Field, AnyUrl


class Settings(BaseSettings):
    dogapi_base_url: AnyUrl = Field(
        default="https://dogapi.dog/api/v2",
        env="DOGAPI_BASE_URL",
        description="Base URL for the external Dog API",
    )
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
---