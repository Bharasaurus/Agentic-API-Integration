import os
from pydantic_settings import BaseSettings
from pydantic import Field, AnyUrl

class Settings(BaseSettings):
    facts_api_base_url: AnyUrl = Field(..., env="FACTS_API_BASE_URL")
    http_timeout: float = Field(10.0, env="HTTP_TIMEOUT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    return Settings()