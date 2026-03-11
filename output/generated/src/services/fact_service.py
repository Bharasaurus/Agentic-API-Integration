from __future__ import annotations

from typing import List

import httpx
from fastapi import Depends, HTTPException, status

from src.clients.fact_client import FactClient
from src.models.fact import FactData, FactAttributes, FactResponse


class FactService:
    """Domain service that encapsulates business logic for facts."""

    def __init__(
        self,
        client: FactClient = Depends(),
        http_client: httpx.AsyncClient = Depends(),
    ):
        self._client = client
        self._http = http_client

    async def get_facts(self) -> FactResponse:
        """
        Retrieve facts from the external service and map them to internal Pydantic models.

        Returns:
            FactResponse: Validated response model.

        Raises:
            HTTPException: 502 if the external payload cannot be parsed.
        """
        raw_facts = await self._client.fetch_facts(self._http)

        # Transform raw dicts into FactData instances, letting Pydantic validate.
        try:
            fact_items = [FactData(**item) for item in raw_facts]
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Invalid data format received from facts service: {exc}",
            ) from exc

        return FactResponse(data=fact_items)