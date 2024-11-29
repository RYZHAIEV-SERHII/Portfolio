from pydantic import BaseModel


class ResumeLinkResponse(BaseModel):
    """A Pydantic model for representing a resume link."""

    link: str

    class Config:
        from_attributes = True


class UpdateResumeLinkResponse(BaseModel):
    """A Pydantic model for representing the response after updating a resume link."""

    message: str
    updated_resume: ResumeLinkResponse

    class Config:
        from_attributes = True
