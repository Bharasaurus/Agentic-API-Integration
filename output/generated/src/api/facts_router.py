from __future__ import annotations

from fastapi import APIRouter, Depends, status

from src.models.fact import FactResponse
from src.services.fact_service import FactService

router = APIRouter(prefix="/facts", tags=["facts"])


@router.get(
    "",
    response_model=FactResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a list of facts",
    response_description="A list of fact resources",
)
async def get_facts(service: FactService = Depends()) -> FactResponse:
    """
    Endpoint to fetch facts.

    Delegates to the FactService which handles external communication and validation.
    """
    return await service.get_facts()