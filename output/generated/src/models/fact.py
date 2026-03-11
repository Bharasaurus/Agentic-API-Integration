from __future__ import annotations

from typing import Literal, List
from uuid import UUID

from pydantic import BaseModel, Field, validator


class FactAttributes(BaseModel):
    """Attributes of a fact."""

    body: str = Field(..., min_length=1, description="The textual content of the fact")

    @validator("body")
    def strip_body(cls, v: str) -> str:
        return v.strip()


class FactData(BaseModel):
    """Single fact resource."""

    id: UUID = Field(..., description="Unique identifier of the fact")
    type: Literal["fact"] = Field("fact", const=True)
    attributes: FactAttributes = Field(..., description="Fact attributes")


class FactResponse(BaseModel):
    """Response model for the /facts endpoint."""

    data: List[FactData] = Field(..., description="List of fact resources")