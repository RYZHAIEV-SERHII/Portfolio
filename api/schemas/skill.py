from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SkillCategorySchema(BaseModel):
    """A Pydantic model for representing a skill category."""

    id: int
    name: str


class SkillSchema(BaseModel):
    """A Pydantic model for representing a skill."""

    id: int
    user_id: int
    skill_category_id: int
    skill_name: str
    proficiency_level: str
    created_at: Optional[datetime]
    skill_category: Optional[SkillCategorySchema]

    class Config:
        from_attributes = True


class CreateSkillResponse(BaseModel):
    """A Pydantic model for representing the response after creating a skill."""

    message: str
    created_skill: SkillSchema


class UpdateSkillResponse(BaseModel):
    """A Pydantic model for representing the response after updating a skill."""

    message: str
    updated_skill: SkillSchema


class DeleteSkillResponse(BaseModel):
    """A Pydantic model for representing the response after deleting a skill."""

    message: str
    deleted_skill: Optional[SkillSchema] = None
