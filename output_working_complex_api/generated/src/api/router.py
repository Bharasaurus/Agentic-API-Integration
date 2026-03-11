from fastapi import APIRouter, Depends, Path, HTTPException, status
from uuid import UUID
from src.services.breed_service import BreedService, get_breed_service
from src.schemas.breed import BreedResponse

router = APIRouter()

@router.get(
    "/{breed_id}",
    response_model=BreedResponse,
    responses={
        200: {"description": "successful"},
        404: {"description": "not-found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_breed(
    breed_id: UUID = Path(..., description="UUID of the breed to retrieve"),
    service: BreedService = Depends(get_breed_service),
) -> BreedResponse:
    """
    Retrieve a dog breed by its UUID.
    """
    return await service.get_breed(breed_id)