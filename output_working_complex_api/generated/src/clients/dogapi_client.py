import httpx
from uuid import UUID
from typing import Any, Dict
from src.core.config import get_settings, Settings

class DogAPIClient:
    def __init__(self, settings: Settings):
        self.base_url = settings.dogapi_base_url.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=10.0)

    async def get_breed(self, breed_id: UUID) -> Dict[str, Any]:
        """
        Calls the external Dog API to retrieve a breed by its UUID.
        """
        endpoint = f"/breeds/{breed_id}"
        response = await self._client.get(endpoint)
        if response.status_code == 404:
            raise httpx.HTTPStatusError("Breed not found", request=response.request, response=response)
        response.raise_for_status()
        return response.json()

    async def aclose(self) -> None:
        await self._client.aclose()

# Dependency provider for the client
async def get_dogapi_client() -> DogAPIClient:
    settings = get_settings()
    client = DogAPIClient(settings)
    try:
        yield client
    finally:
        await client.aclose()