import os
from pydantic import BaseSettings, Field, AnyUrl, SecretStr

class Settings(BaseSettings):
    dogapi_base_url: AnyUrl = Field(
        default="https://dogapi.dog/api/v2",
        description="Base URL for the external Dog API",
    )
    log_level: str = Field(default="INFO", description="Logging level")
    http_timeout: float = Field(default=10.0, description="HTTP client timeout in seconds")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    return Settings()