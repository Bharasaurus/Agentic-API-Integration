from __future__ import annotations
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, validator, HttpUrl

class BreedData(BaseModel):
    id: UUID
    type: str = Field(..., const=True, pattern="^breed$")

class BreedsRelationship(BaseModel):
    data: List[BreedData]

class GroupRelationships(BaseModel):
    breeds: BreedsRelationship

class GroupAttributes(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)

class GroupData(BaseModel):
    id: UUID
    type: str = Field(..., const=True, pattern="^group$")
    attributes: GroupAttributes
    relationships: GroupRelationships

class Links(BaseModel):
    self: HttpUrl
    current: HttpUrl
    next: Optional[HttpUrl] = None
    last: HttpUrl

class GroupsResponse(BaseModel):
    data: List[GroupData]
    links: Links

    @validator("data", each_item=True)
    def validate_group(cls, v: GroupData) -> GroupData:
        # Additional domain validation can be added here
        return v