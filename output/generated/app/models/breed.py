from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class WeightRange(BaseModel):
    min: int = Field(..., ge=0, description="Minimum weight in kilograms")
    max: int = Field(..., ge=0, description="Maximum weight in kilograms")

    @field_validator("max")
    def max_not_less_than_min(cls, v: int, values):
        if "min" in values and v < values["min"]:
            raise ValueError("max must be greater than or equal to min")
        return v


class LifeRange(BaseModel):
    min: int = Field(..., ge=0, description="Minimum lifespan in years")
    max: int = Field(..., ge=0, description="Maximum lifespan in years")

    @field_validator("max")
    def max_not_less_than_min(cls, v: int, values):
        if "min" in values and v < values["min"]:
            raise ValueError("max must be greater than or equal to min")
        return v


class BreedAttributes(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    hypoallergenic: bool
    life: LifeRange
    male_weight: WeightRange
    female_weight: WeightRange

    model_config = ConfigDict(extra="forbid")


class BreedData(BaseModel):
    id: str = Field(..., description="UUID of the breed")
    type: Literal["breed"] = "breed"
    attributes: BreedAttributes

    model_config = ConfigDict(extra="forbid")


class Pagination(BaseModel):
    current: int = Field(..., ge=1)
    records: int = Field(..., ge=0)


class Links(BaseModel):
    self: str = Field(..., description="Link to the current collection")
    current: str
    next: Optional[str] = None
    last: str


class Meta(BaseModel):
    pagination: Pagination


class BreedResponse(BaseModel):
    data: List[BreedData]
    meta: Meta
    links: Links

    model_config = ConfigDict(extra="forbid")
---