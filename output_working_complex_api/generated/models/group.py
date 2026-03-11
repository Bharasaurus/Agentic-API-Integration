from __future__ import annotations

from typing import List, Literal
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl, validator

class BreedData(BaseModel):
    id: UUID
    type: Literal["breed"]

class Breeds(BaseModel):
    data: List[BreedData]

class Relationships(BaseModel):
    breeds: Breeds

class Attributes(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)

class GroupData(BaseModel):
    id: UUID
    type: Literal["group"]
    attributes: Attributes
    relationships: Relationships

class Links(BaseModel):
    self: HttpUrl

class GroupResponse(BaseModel):
    data: GroupData
    links: Links