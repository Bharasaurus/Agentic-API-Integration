from fastapi import APIRouter, Depends, HTTPException, status

from services.group_service import GroupService, get_group_service
from models.group import GroupResponse

router = APIRouter(prefix="/groups", tags=["groups"])

@router.get(
    "/",
    response_model=GroupResponse,
    responses={
        200: {"description": "successful"},
        502: {"description": "Bad Gateway - upstream service error"},
        500: {"description": "Internal Server Error"},
    },
    status_code=status.HTTP_200_OK,
)
async def list_groups(
    service: GroupService = Depends(get_group_service),
) -> GroupResponse:
    try:
        return await service.get_groups()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(exc)}",
        )