from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.fact import FactResponse, Fact
from app.services.fact_service import FactService
from app.dependencies import get_fact_service

router = APIRouter(prefix="/facts", tags=["facts"])

@router.get(
    "",
    response_model=FactResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a list of facts",
)
async def get_facts(
    service: FactService = Depends(get_fact_service),
) -> FactResponse:
    try:
        facts: List[Fact] = await service.fetch_facts()
        return FactResponse(data=facts)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc