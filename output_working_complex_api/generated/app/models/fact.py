from __future__ import annotations
from typing import List
from uuid import UUID
from pydantic import BaseModel, Field, validator

class FactAttributes(BaseModel):
    body: str = Field(..., min_length=1, description="The fact text")

class Fact(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the fact")
    type: str = Field(..., description="Resource type, must be 'fact'")
    attributes: FactAttributes

    @validator("type")
    def type_must_be_fact(cls, v: str) -> str:
        if v != "fact":
            raise ValueError("type must be 'fact'")
        return v

class FactResponse(BaseModel):
    data: List[Fact] = Field(..., description="List of facts")