from fastapi import APIRouter, Depends, Path, HTTPException, status

from services.breed_service import BreedService, get_breed_service
from schemas.breed import BreedResponse

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
    breed_id: str = Path(..., description="UUID of the breed", regex=r"^[0-9a-fA-F-]{36}$"),
    service: BreedService = Depends(get_breed_service),
) -> BreedResponse:
    """
    Retrieve a dog breed by its UUID.
    """
    try:
        return await service.get_breed(breed_id)
    except HTTPException:
        # Propagate HTTPExceptions raised by lower layers (e.g., 404)
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {exc}",
        ) from exc