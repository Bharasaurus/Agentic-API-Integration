from typing import AsyncGenerator

import httpx
from fastapi import Depends

from config import settings

async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(base_url=str(settings.DOGAPI_BASE_URL), timeout=10.0) as client:
        yield client


async def get_async_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(base_url=str(settings.PET_SERVICE_BASE_URL), timeout=10.0) as client:
        yield client