from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from services.group_service import GroupService
from models.group import GroupResponse

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
    group_id: UUID = Path(..., description="UUID of the group"),
    service: GroupService = Depends(),
) -> GroupResponse:
    try:
        return await service.get_group(group_id)
    except HTTPException as exc:
        # Propagate known HTTPExceptions (e.g., 404)
        raise exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from exc