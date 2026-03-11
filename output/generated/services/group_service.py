from typing import Optional
from fastapi import HTTPException, status, Depends
from clients.dogapi_client import DogApiClient, get_dogapi_client
from schemas.group import GroupResponse

class GroupService:
    def __init__(self, client: DogApiClient = Depends(get_dogapi_client)):
        self.client = client

    async def fetch_group(self, group_id: str) -> GroupResponse:
        try:
            raw = await self.client.get_group(group_id)
            return GroupResponse.model_validate(raw)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Group not found",
                )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error communicating with external Dog API",
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            )