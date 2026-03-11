from __future__ import annotations
from typing import List
import httpx
from httpx import AsyncClient, Response, HTTPError
from app.models.fact import Fact
from app.config import Settings

class FactClient:
    def __init__(self, settings: Settings, http_client: AsyncClient) -> None:
        self._base_url = settings.facts_api_base_url.rstrip("/")
        self._client = http_client

    async def get_facts(self) -> List[Fact]:
        url = f"{self._base_url}/facts"
        try:
            response: Response = await self._client.get(url, timeout=self._client.timeout)
            response.raise_for_status()
        except HTTPError as exc:
            raise RuntimeError(f"Failed to fetch facts from external service: {exc}") from exc

        json_data = response.json()
        # Expecting structure: {"data": [{...}, ...]}
        return [Fact(**item) for item in json_data.get("data", [])]