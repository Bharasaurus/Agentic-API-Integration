from typing import List
from httpx import AsyncClient, HTTPError
from fastapi import Depends, HTTPException, status

from src.models.dogapi import GroupsResponse
from src.dependencies import get_async_http_client

class DogApiClient:
    def __init__(self, client: AsyncClient):
        self._client = client

    async def fetch_groups(self) -> GroupsResponse:
        try:
            response = await self._client.get("/groups")
            response.raise_for_status()
            payload = response.json()
            return GroupsResponse.model_validate(payload)
        except HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to fetch groups from external service: {exc}",
            ) from exc

async def get_dogapi_client(
    client: AsyncClient = Depends(get_async_http_client),
) -> DogApiClient:
    return DogApiClient(client)