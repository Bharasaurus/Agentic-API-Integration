import httpx
from typing import Any, Dict
from fastapi import Depends
from config import get_settings, Settings

class DogApiClient:
    def __init__(self, settings: Settings = Depends(get_settings)):
        self.base_url = settings.dogapi_base_url
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=10.0)

    async def get_group(self, group_id: str) -> Dict[str, Any]:
        url = f"/api/v2/groups/{group_id}"
        response = await self._client.get(url)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self._client.aclose()

# Dependency provider for FastAPI
async def get_dogapi_client(
    client: DogApiClient = Depends(DogApiClient),
) -> DogApiClient:
    try:
        yield client
    finally:
        await client.close()