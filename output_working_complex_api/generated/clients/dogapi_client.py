from typing import Any

import httpx
from fastapi import Depends, HTTPException, status

from config import settings
from models.group import GroupResponse

class DogApiClient:
    def __init__(self, client: httpx.AsyncClient = None):
        self._client = client or httpx.AsyncClient(base_url=str(settings.DOGAPI_BASE_URL))

    async def fetch_group(self, group_id: str) -> GroupResponse:
        url = f"/groups/{group_id}"
        try:
            response = await self._client.get(url)
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error contacting Dog API: {exc}",
            ) from exc

        if response.status_code == status.HTTP_200_OK:
            try:
                json_data = response.json()
                return GroupResponse.model_validate(json_data)
            except Exception as exc:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Invalid response format from Dog API",
                ) from exc
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Unexpected error from Dog API (status {response.status_code})",
            )