from uuid import UUID
from src.clients.dogapi_client import DogAPIClient
from src.schemas.breed import BreedResponse
from fastapi import HTTPException, status

class BreedService:
    def __init__(self, client: DogAPIClient):
        self.client = client

    async def get_breed(self, breed_id: UUID) -> BreedResponse:
        """
        Retrieves a breed from the external API and parses it into a Pydantic model.
        """
        try:
            raw = await self.client.get_breed(breed_id)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Breed not found")
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="External service error")
        # The external API already returns a JSON structure compatible with our schema,
        # but we enforce validation by constructing the model.
        return BreedResponse.model_validate(raw)

# Dependency provider for the service
def get_breed_service(client: DogAPIClient = Depends(get_dogapi_client)) -> BreedService:
    return BreedService(client)