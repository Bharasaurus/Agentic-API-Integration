from typing import Any
import httpx
from fastapi import Depends, HTTPException, status

from ..models.breed import BreedsResponse
from ..dependencies import get_http_client

class DogApiClient:
    def __init__(self, http_client: httpx.AsyncClient = Depends(get_http_client)):
        self._client = http_client

    async def get_breeds(self) -> BreedsResponse:
        try:
            response = await self._client.get("/breeds")
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Dog API returned error: {exc.response.status_code}"
            ) from exc
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error communicating with Dog API: {str(exc)}"
            ) from exc

        try:
            payload: Any = response.json()
            return BreedsResponse.model_validate(payload)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid response format from Dog API"
            ) from exc