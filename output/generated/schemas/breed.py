from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, validator

class LifeSpan(BaseModel):
    min: int = Field(..., ge=0, description="Minimum lifespan in years")
    max: int = Field(..., ge=0, description="Maximum lifespan in years")

    @validator("max")
    def max_not_less_than_min(cls, v, values):
        if "min" in values and v < values["min"]:
            raise ValueError("max must be greater than or equal to min")
        return v

class WeightRange(BaseModel):
    min: int = Field(..., ge=0, description="Minimum weight in kilograms")
    max: int = Field(..., ge=0, description="Maximum weight in kilograms")

    @validator("max")
    def max_not_less_than_min(cls, v, values):
        if "min" in values and v < values["min"]:
            raise ValueError("max must be greater than or equal to min")
        return v

class BreedAttributes(BaseModel):
    name: str = Field(..., min_length=1)
    life: LifeSpan
    male_weight: WeightRange = Field(..., alias="male_weight")
    female_weight: WeightRange = Field(..., alias="female_weight")
    description: str = Field(..., min_length=1)
    hypoallergenic: bool

class BreedData(BaseModel):
    id: UUID
    type: Literal["breed"]
    attributes: BreedAttributes

class Links(BaseModel):
    self: str = Field(..., alias="self")

class BreedResponse(BaseModel):
    data: BreedData
    links: Links