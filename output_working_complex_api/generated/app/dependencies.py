from __future__ import annotations
import httpx
from fastapi import Depends
from app.config import Settings, get_settings

async def get_http_client(settings: Settings = Depends(get_settings)) -> httpx.AsyncClient:
    async with httpx.AsyncClient(timeout=settings.http_timeout) as client:
        yield client

def get_fact_client(
    settings: Settings = Depends(get_settings),
    http_client: httpx.AsyncClient = Depends(get_http_client),
) -> FactClient:
    return FactClient(settings=settings, http_client=http_client)

def get_fact_service(
    client: FactClient = Depends(get_fact_client),
) -> FactService:
    return FactService(client=client)