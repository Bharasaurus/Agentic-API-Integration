from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, validator

class BreedIdentifier(BaseModel):
    id: str = Field(..., description="Breed UUID")
    type: Literal["breed"] = "breed"

class Relationships(BaseModel):
    breeds: dict = Field(..., description="Breeds relationship")

    @validator("breeds")
    def validate_breeds(cls, v: dict) -> dict:
        if "data" not in v or not isinstance(v["data"], list):
            raise ValueError("breeds must contain a 'data' list")
        return v

class Attributes(BaseModel):
    name: str = Field(..., description="Group name")

class GroupData(BaseModel):
    id: str = Field(..., description="Group UUID")
    type: Literal["group"] = "group"
    attributes: Attributes
    relationships: Relationships

class Links(BaseModel):
    self: str = Field(..., alias="self")

class GroupResponse(BaseModel):
    data: GroupData
    links: Links