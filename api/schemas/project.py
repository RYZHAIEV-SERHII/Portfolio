from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ImageSchema(BaseModel):
    """A Pydantic model for representing an image."""

    id: Optional[int]
    name: str
    url: str
    image_category_id: int


class ProjectSchema(BaseModel):
    """A Pydantic model for representing a project."""

    id: Optional[int]
    user_id: int
    title: str
    description: str
    tech_stack: str
    url: str
    created_at: Optional[datetime]
    project_category_id: int
    images: Optional[List[ImageSchema]]

    class Config:
        from_attributes = True


class CreateProjectResponse(BaseModel):
    """A Pydantic model for representing the response after creating a project."""

    message: str
    created_project: ProjectSchema


class UpdateProjectResponse(BaseModel):
    """A Pydantic model for representing the response after updating a project."""

    message: str
    updated_project: ProjectSchema


class DeleteProjectResponse(BaseModel):
    """A Pydantic model for representing the response after deleting a project."""

    message: str
    deleted_project: Optional[ProjectSchema] = None
