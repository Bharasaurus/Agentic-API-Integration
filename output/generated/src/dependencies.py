import httpx
from fastapi import Depends
from src.config import Settings, get_settings

async def get_async_http_client(
    settings: Settings = Depends(get_settings),
) -> httpx.AsyncClient:
    async with httpx.AsyncClient(
        base_url=str(settings.dogapi_base_url),
        timeout=settings.http_timeout,
        follow_redirects=True,
    ) as client:
        yield client