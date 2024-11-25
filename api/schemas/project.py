from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ImageSchema(BaseModel):
    """A Pydantic model for representing an image."""

    id: int
    name: str
    image_source: str
    file_data: Optional[bytes]
    url: Optional[str]


class ProjectSchema(BaseModel):
    """A Pydantic model for representing a project."""

    id: int
    user_id: int
    title: str
    description: str
    tech_stack: str
    url: str
    created_at: datetime
    project_category_id: int
    images: List[ImageSchema]

    class Config:
        from_attributes = True
