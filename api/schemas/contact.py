from typing import List

from pydantic import BaseModel


class SocialProfile(BaseModel):
    """
    A Pydantic model representing a social profile.
    """

    name: str
    url: str


class ContactInfoResponse(BaseModel):
    """
    A Pydantic model representing the response schema for contact information.
    """

    address: str
    social_profiles: List[SocialProfile]
    email: str
    phone: str
    notification: str

    class Config:
        from_attributes = True
