from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExperienceSchema(BaseModel):
    """A Pydantic model for representing an experience."""

    id: int
    user_id: int
    company_name: str
    role: str
    start_date: datetime
    end_date: Optional[datetime] = None
    description: str

    class Config:
        from_attributes = True


class CreateExperienceResponse(BaseModel):
    """A Pydantic model for representing the response after creating an experience."""

    message: str
    created_experience: ExperienceSchema


class UpdateExperienceResponse(BaseModel):
    """A Pydantic model for representing the response after updating an experience."""

    message: str
    updated_experience: ExperienceSchema


class DeleteExperienceResponse(BaseModel):
    """A Pydantic model for representing the response after deleting an experience."""

    message: str
    deleted_experience: Optional[ExperienceSchema] = None
