from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, validator, ConfigDict

class LifeSpan(BaseModel):
    min: int = Field(..., ge=0)
    max: int = Field(..., ge=0)

    @validator("max")
    def max_not_less_than_min(cls, v, values):
        if "min" in values and v < values["min"]:
            raise ValueError("max must be greater than or equal to min")
        return v

class WeightRange(BaseModel):
    min: int = Field(..., ge=0)
    max: int = Field(..., ge=0)

    @validator("max")
    def max_not_less_than_min(cls, v, values):
        if "min" in values and v < values["min"]:
            raise ValueError("max must be greater than or equal to min")
        return v

class BreedAttributes(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    hypoallergenic: bool
    life: LifeSpan
    male_weight: WeightRange
    female_weight: WeightRange

class BreedData(BaseModel):
    id: str = Field(..., pattern=r"^[0-9a-fA-F-]{36}$")
    type: Literal["breed"]
    attributes: BreedAttributes

class Pagination(BaseModel):
    current: int = Field(..., ge=1)
    records: int = Field(..., ge=0)

class Meta(BaseModel):
    pagination: Pagination

class Links(BaseModel):
    self: str = Field(..., description="Current request URL")
    current: str
    next: Optional[str] = None
    last: str

class BreedsResponse(BaseModel):
    data: List[BreedData]
    meta: Meta
    links: Links

    model_config = ConfigDict(
        json_encoders={},
        populate_by_name=True,
        extra="forbid"
    )