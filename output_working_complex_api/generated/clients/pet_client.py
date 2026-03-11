from __future__ import annotations

import httpx
from typing import Any

from fastapi import HTTPException, status

class PetServiceClient:
    """
    A thin wrapper around `httpx.AsyncClient` that knows how to talk to the
    external pet service.
    """

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._client = http_client

    async def create_pet(self, payload: dict[str, Any]) -> None:
        """
        Sends a POST request to the external `/pets` endpoint.

        Args:
            payload: The JSON payload to forward.

        Raises:
            HTTPException: If the external service returns a non‑2xx response.
        """
        try:
            response = await self._client.post("pets", json=payload)
        except httpx.RequestError as exc:
            # Network‑level error
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to communicate with pet service: {exc}",
            ) from exc

        if response.status_code != status.HTTP_201_CREATED:
            # Propagate error details from the upstream service if available
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Pet service error"),
            )
        # No return value needed; a 201 indicates success.
