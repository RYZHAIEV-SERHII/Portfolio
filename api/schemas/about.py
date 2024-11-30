from pydantic import BaseModel
from typing import List


class AboutInfoResponse(BaseModel):
    """
    Response schema for the API endpoint that returns the user's about information.
    """

    info: str


class AboutInterestsResponse(BaseModel):
    """
    Response schema for the API endpoint that returns the user's interests.
    """

    interests: List[str]
