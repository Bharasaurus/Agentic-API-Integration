import httpx
from fastapi import Depends
from app.config import get_settings, Settings


async def get_http_client(settings: Settings = Depends(get_settings)) -> httpx.AsyncClient:
    """
    Provides a single httpx.AsyncClient instance configured with the base URL.
    The client is closed automatically by FastAPI's lifespan events.
    """
    async with httpx.AsyncClient(base_url=str(settings.dogapi_base_url), timeout=10.0) as client:
        yield client
---