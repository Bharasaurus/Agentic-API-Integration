from fastapi import APIRouter, Depends, HTTPException, status
import httpx

from models.pet import PetCreateRequest
from clients.pet_client import PetServiceClient
from dependencies import get_async_http_client

router = APIRouter()


async def get_pet_service_client(
    http_client: httpx.AsyncClient = Depends(get_async_http_client),
) -> PetServiceClient:
    """Dependency that provides a ready‑to‑use `PetServiceClient`."""
    return PetServiceClient(http_client)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "Pet created"}},
)
async def create_pet(
    request: PetCreateRequest,
    client: PetServiceClient = Depends(get_pet_service_client),
) -> None:
    """
    Create a new pet by forwarding the request to the external pet service.

    Returns:
        201 Created on success.
    """
    payload = {"content": request.content}
    await client.create_pet(payload)
    # FastAPI automatically returns an empty body with the 201 status.
