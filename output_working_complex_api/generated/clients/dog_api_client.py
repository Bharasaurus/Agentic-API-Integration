from typing import Any

import httpx
from fastapi import Depends, HTTPException, status

from dependencies import get_http_client
from models.group import GroupResponse

class DogApiClient:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def fetch_groups(self) -> GroupResponse:
        try:
            response = await self._client.get("/v2/groups")
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error from Dog API: {exc.response.text}",
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Unable to connect to Dog API: {str(exc)}",
            )
        data: Any = response.json()
        return GroupResponse.model_validate(data)

async def get_dog_api_client(
    client: httpx.AsyncClient = Depends(get_http_client),
) -> DogApiClient:
    return DogApiClient(client)