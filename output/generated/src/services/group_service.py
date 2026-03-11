from fastapi import Depends

from src.clients.dogapi_client import DogApiClient, get_dogapi_client
from src.models.dogapi import GroupsResponse

class GroupService:
    def __init__(self, dogapi_client: DogApiClient):
        self._dogapi_client = dogapi_client

    async def get_all_groups(self) -> GroupsResponse:
        return await self._dogapi_client.fetch_groups()

async def get_group_service(
    dogapi_client: DogApiClient = Depends(get_dogapi_client),
) -> GroupService:
    return GroupService(dogapi_client)