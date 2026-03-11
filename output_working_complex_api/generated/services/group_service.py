from uuid import UUID

from fastapi import Depends, HTTPException, status

from clients.dogapi_client import DogApiClient
from models.group import GroupResponse

class GroupService:
    def __init__(self, dogapi_client: DogApiClient = Depends()):
        self._client = dogapi_client

    async def get_group(self, group_id: UUID) -> GroupResponse:
        return await self._client.fetch_group(str(group_id))

    async def get_groups(self) -> GroupResponse:
        """Fetch all groups from the external API."""
        return await self._client.fetch_groups()


def get_group_service(dogapi_client: DogApiClient = Depends()) -> GroupService:
    """Dependency that provides a ready-to-use GroupService."""
    return GroupService(dogapi_client)