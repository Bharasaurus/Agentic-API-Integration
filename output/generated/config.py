import os
from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    dogapi_base_url: str = Field(..., alias="DOGAPI_BASE_URL")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # ✅ Pydantic v2 config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("dogapi_base_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError("DOGAPI_BASE_URL must be a valid URL")
        return v.rstrip("/")


@lru_cache()
def get_settings() -> Settings:
    return Settings()