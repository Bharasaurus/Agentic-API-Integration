from fastapi import Depends

from clients.dog_api_client import DogApiClient, get_dog_api_client
from schemas.breed import BreedResponse

class BreedService:
    def __init__(self, api_client: DogApiClient):
        self._api_client = api_client

    async def get_breed(self, breed_id: str) -> BreedResponse:
        """
        Business logic for retrieving a breed.
        Currently a thin wrapper around the external client, but kept for future extensibility.
        """
        return await self._api_client.fetch_breed(breed_id)

async def get_breed_service(
    api_client: DogApiClient = Depends(get_dog_api_client),
) -> BreedService:
    return BreedService(api_client)