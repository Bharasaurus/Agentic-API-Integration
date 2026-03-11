from pydantic import BaseModel, Field, validator
from uuid import UUID
from typing import Optional

class LifeSpan(BaseModel):
    min: int = Field(..., ge=0, description="Minimum life expectancy in years")
    max: int = Field(..., ge=0, description="Maximum life expectancy in years")

    @validator("max")
    def max_not_less_than_min(cls, v, values):
        if "min" in values and v < values["min"]:
            raise ValueError("max must be greater than or equal to min")
        return v

class Weight(BaseModel):
    min: int = Field(..., ge=0, description="Minimum weight in kilograms")
    max: int = Field(..., ge=0, description="Maximum weight in kilograms")

    @validator("max")
    def max_not_less_than_min(cls, v, values):
        if "min" in values and v < values["min"]:
            raise ValueError("max must be greater than or equal to min")
        return v

class BreedAttributes(BaseModel):
    name: str = Field(..., description="Breed name")
    life: LifeSpan = Field(..., description="Life expectancy")
    male_weight: Weight = Field(..., description="Male weight range")
    female_weight: Weight = Field(..., description="Female weight range")
    description: str = Field(..., description="Short description of the breed")
    hypoallergenic: bool = Field(..., description="Whether the breed is hypoallergenic")

class BreedData(BaseModel):
    id: UUID = Field(..., description="Breed identifier")
    type: str = Field(..., const=True, description="Resource type, always 'breed'")
    attributes: BreedAttributes = Field(..., description="Breed attributes")

class Links(BaseModel):
    self: str = Field(..., description="Self link to the resource")

class BreedResponseContent(BaseModel):
    data: BreedData = Field(..., description="Primary data object")
    links: Links = Field(..., description="Related links")

class BreedResponse(BaseModel):
    data: BreedResponseContent = Field(..., description="Full response payload")