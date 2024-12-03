from datetime import date
from typing import Optional, List

from pydantic import BaseModel, field_validator, Field


class EducationInfoResponse(BaseModel):
    """A Pydantic model for representing education information."""

    institution_name: str
    degree: str
    field_of_study: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str]
    relevant_coursework: Optional[List[str]]
    skills_acquired: Optional[List[str]]
    diploma: Optional[str]

    class Config:
        from_attributes = True


class CertificationInfoResponse(BaseModel):
    """A Pydantic model for representing certification information."""

    id: int
    user_id: int
    name: str
    issuing_organization: str
    issue_date: date
    credential_id: Optional[str]
    credential_url: Optional[str]
    skills_acquired: Optional[List[str]] = Field(None, alias="skills_acquired")

    # Convert comma-separated string, which is defined in database, to list of strings for better representation
    _convert_skills_acquired = field_validator("skills_acquired", mode="before")(
        lambda v: (
            [skill.strip() for skill in str(v).split(",")] if isinstance(v, str) else v
        )
    )

    class Config:
        from_attributes = True


class CreateCertificationResponse(BaseModel):
    """A Pydantic model for representing the response after creating a certification."""

    message: str
    created_certification: CertificationInfoResponse


class UpdateCertificationResponse(BaseModel):
    """A Pydantic model for representing the response after updating a certification."""

    message: str
    updated_certification: CertificationInfoResponse


class DeleteCertificationResponse(BaseModel):
    """A Pydantic model for representing the response after deleting a certification."""

    message: str
    deleted_certification: Optional[CertificationInfoResponse] = None
