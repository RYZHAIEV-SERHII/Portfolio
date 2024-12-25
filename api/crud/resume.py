from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.db import database
from logging_setup import api_logger
from src.db.models import Resume


async def get_resume_link(db: Session = Depends(database.get_db_session)) -> Resume:
    """
    Retrieve the resume instance from the database.

    Args:
        db (Session): The database session.

    Returns:
        Resume: The resume instance.

    Raises:
        HTTPException: If the resume is not found.
    """
    resume = db.query(Resume).first()
    if not resume:
        api_logger.error("Resume not found")
        raise HTTPException(status_code=404, detail="Resume not found")
    api_logger.info("Resume retrieved")
    return resume


async def update_resume_link(
    link: str, db: Session = Depends(database.get_db_session)
) -> Resume:
    """
    Update the resume link in the database.

    Args:
        link (str): The new link to update.
        db (Session): The database session.

    Returns:
        Resume: The updated resume instance.

    Raises:
        HTTPException: If the resume is not found.
    """
    resume = db.query(Resume).first()
    if not resume:
        api_logger.error("Resume not found")
        raise HTTPException(status_code=404, detail="Resume not found")
    resume.link = link
    db.commit()
    db.refresh(resume)
    api_logger.info("Resume updated")

    return resume
