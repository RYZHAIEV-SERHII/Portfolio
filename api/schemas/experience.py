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
