from functools import lru_cache

import httpx
from fastapi import Depends

from config import Settings

@lru_cache()
def get_settings() -> Settings:
    return Settings()

async def get_http_client(settings: Settings = Depends(get_settings)) -> httpx.AsyncClient:
    async with httpx.AsyncClient(base_url=settings.dogapi_base_url, timeout=10.0) as client:
        yield client