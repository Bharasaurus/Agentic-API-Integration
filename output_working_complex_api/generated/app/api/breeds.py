from fastapi import APIRouter, Depends, HTTPException, status

from ..services.dog_api_client import DogApiClient
from ..models.breed import BreedsResponse

router = APIRouter(prefix="/breeds", tags=["Breeds"])

@router.get(
    "",
    response_model=BreedsResponse,
    responses={200: {"description": "successful"}},
    status_code=status.HTTP_200_OK,
    summary="Retrieve list of dog breeds"
)
async def list_breeds(
    client: DogApiClient = Depends()
) -> BreedsResponse:
    """
    Proxy endpoint that forwards the request to the external Dog API
    and returns a validated response.
    """
    return await client.get_breeds()