from __future__ import annotations
from typing import List
from app.clients.fact_client import FactClient
from app.models.fact import Fact

class FactService:
    def __init__(self, client: FactClient) -> None:
        self._client = client

    async def fetch_facts(self) -> List[Fact]:
        return await self._client.get_facts()