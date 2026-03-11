from fastapi import APIRouter, Depends, Path, status
from services.group_service import GroupService
from schemas.group import GroupResponse

router = APIRouter(prefix="/groups", tags=["groups"])

@router.get(
    "/{group_id}",
    response_model=GroupResponse,
    responses={
        200: {"description": "successful"},
        404: {"description": "not-found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_group(
    group_id: str = Path(..., description="UUID of the group"),
    service: GroupService = Depends(),
) -> GroupResponse:
    """
    Retrieve a group by its UUID.
    """
    return await service.fetch_group(group_id)