from typing import Any
import httpx
from fastapi import Depends, HTTPException, status
from app.models.breed import BreedResponse
from app.dependencies import get_http_client


class DogAPIClient:
    """
    Thin wrapper around httpx.AsyncClient for the external Dog API.
    """

    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def get_breeds(self) -> BreedResponse:
        """
        Calls the external `/breeds` endpoint and returns a validated BreedResponse.
        Raises HTTPException with 502 if the external service fails or returns invalid data.
        """
        try:
            response: httpx.Response = await self._client.get("/breeds")
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error contacting Dog API: {exc}",
            ) from exc

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Dog API returned unexpected status {response.status_code}",
            )

        try:
            json_body: Any = response.json()
            return BreedResponse.model_validate(json_body)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to parse Dog API response: {exc}",
            ) from exc


async def get_dogapi_client(
    client: httpx.AsyncClient = Depends(get_http_client),
) -> DogAPIClient:
    return DogAPIClient(client)
---