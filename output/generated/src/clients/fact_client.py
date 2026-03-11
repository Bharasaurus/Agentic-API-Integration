from __future__ import annotations

from typing import List, Dict, Any

import httpx
from fastapi import Depends, HTTPException, status

from src.config import get_settings, Settings


class FactClient:
    """HTTP client responsible for communicating with the external facts service."""

    def __init__(self, settings: Settings = Depends(get_settings)):
        self.base_url: str = str(settings.facts_service_base_url).rstrip("/")
        self.timeout: float = settings.http_timeout

    async def fetch_facts(self, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
        """
        Retrieve raw fact objects from the external service.

        Raises:
            HTTPException: 502 Bad Gateway when the external service cannot be reached
                           or returns a non‑2xx status.
        """
        url = f"{self.base_url}/facts"
        try:
            response = await client.get(url, timeout=self.timeout)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to fetch facts from external service: {exc}",
            ) from exc

        # Expecting the external service to return a JSON payload compatible with our models.
        # If the shape differs, a validation error will be raised later in the service layer.
        return response.json().get("data", [])