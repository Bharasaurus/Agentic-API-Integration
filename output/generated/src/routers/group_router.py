from fastapi import APIRouter, Depends, HTTPException, status
from src.services.group_service import GroupService, get_group_service
from src.models.dogapi import GroupsResponse

router = APIRouter()

@router.get(
    "/",
    response_model=GroupsResponse,
    responses={
        200: {"description": "Successful retrieval of groups"},
        502: {"description": "Bad gateway – external service failure"},
    },
    status_code=status.HTTP_200_OK,
)
async def list_groups(
    service: GroupService = Depends(get_group_service),
) -> GroupsResponse:
    """
    Retrieve the list of dog groups from the external Dog API.
    """
    try:
        return await service.get_all_groups()
    except HTTPException:
        # Propagate HTTPException raised by the client layer
        raise
    except Exception as exc:
        # Unexpected errors are mapped to 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc