from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

class PetCreateRequest(BaseModel):
    """
    Request model for creating a pet.
    The API expects a simple string payload (e.g., the pet's name).
    """
    content: str = Field(..., description="The pet's name or description")

    @field_validator("content")
    @classmethod
    def non_empty(cls, v: str) -> str:
        """Ensure the content is not an empty string."""
        if not v.strip():
            raise ValueError("content must not be empty")
        return v
