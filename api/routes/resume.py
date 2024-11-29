from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.crud.resume import get_resume_link, update_resume_link
from api.db import database
from api.schemas.resume import ResumeLinkResponse, UpdateResumeLinkResponse

router = APIRouter(tags=["Resume"])


@router.get("/resume", response_model=ResumeLinkResponse)
async def get_resume_url(db: Session = Depends(database.get_db_session)):
    """
    Retrieve the current resume link from the database.
    """
    resume = await get_resume_link(db)
    return resume


@router.put("/resume", response_model=UpdateResumeLinkResponse)
async def update_resume_url(link: str, db: Session = Depends(database.get_db_session)):
    """
    Update the resume link in the database.
    """
    updated_resume = await update_resume_link(link, db)
    return {
        "message": "Resume link updated successfully",
        "updated_resume": updated_resume,
    }
