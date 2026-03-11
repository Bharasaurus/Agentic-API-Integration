from fastapi import APIRouter, Depends, status
from app.clients.dogapi_client import DogAPIClient, get_dogapi_client
from app.models.breed import BreedResponse

router = APIRouter(prefix="/breeds", tags=["Breeds"])


@router.get(
    "",
    response_model=BreedResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve list of dog breeds",
    response_description="A collection of dog breeds with pagination metadata",
)
async def list_breeds(
    dogapi_client: DogAPIClient = Depends(get_dogapi_client),
) -> BreedResponse:
    """
    Proxy endpoint that forwards the request to the external Dog API,
    validates the payload, and returns it to the caller.
    """
    return await dogapi_client.get_breeds()
---