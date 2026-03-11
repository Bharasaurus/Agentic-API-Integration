from typing import Any

import httpx
from fastapi import Depends, HTTPException, status

from schemas.breed import BreedResponse
from dependencies import get_http_client

class DogApiClient:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def fetch_breed(self, breed_id: str) -> BreedResponse:
        """
        Calls the external Dog API to retrieve a breed by its UUID.
        """
        response = await self._client.get(f"/breeds/{breed_id}")

        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Breed with id {breed_id} not found",
            )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to retrieve breed information from external service",
            )

        # The external API returns a JSON structure that matches our schema
        payload: dict[str, Any] = response.json()
        try:
            breed_response = BreedResponse.model_validate(payload)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Invalid response format from external service: {exc}",
            )
        return breed_response

async def get_dog_api_client(
    client: httpx.AsyncClient = Depends(get_http_client),
) -> DogApiClient:
    return DogApiClient(client)