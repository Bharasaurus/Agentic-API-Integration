import os
from functools import lru_cache
from pydantic import BaseSettings, Field, validator

class Settings(BaseSettings):
    dogapi_base_url: str = Field(..., env="DOGAPI_BASE_URL")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    @validator("dogapi_base_url")
    def validate_url(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError("DOGAPI_BASE_URL must be a valid URL")
        return v.rstrip("/")

@lru_cache()
def get_settings() -> Settings:
    return Settings()