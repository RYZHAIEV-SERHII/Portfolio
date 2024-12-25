from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.db import database
from api.schemas.experience import ExperienceSchema
from logging_setup import api_logger
from src.db.models import Experience


def get_all_experiences(db: Session = Depends(database.get_db_session)):
    """
    Retrieve all experiences from the database.
    """
    api_logger.info("Experiences. Status: retrieved")
    return db.query(Experience).all()


async def get_experience_by_id(
    experience_id: int, db: Session = Depends(database.get_db_session)
):
    """Retrieve an experience by ID"""
    experience = db.query(Experience).get(experience_id)
    if not experience:
        api_logger.error(f"Experience {experience_id} not found")
        raise HTTPException(status_code=404, detail="Experience not found")
    api_logger.info(f"Experience {experience.company_name} retrieved")
    return experience


async def create_experience(
    experience: ExperienceSchema, db: Session = Depends(database.get_db_session)
) -> dict:
    """Create a new experience in the database.

    Args:
        experience (ExperienceSchema): The experience to create.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message "Experience created successfully" and the created experience.
    """
    try:
        new_experience = Experience(
            user_id=experience.user_id,
            company_name=experience.company_name,
            role=experience.role,
            start_date=experience.start_date,
            end_date=experience.end_date,
            description=experience.description,
        )
        db.add(new_experience)
        db.commit()
        db.refresh(new_experience)
        api_logger.info(f"Experience {new_experience.company_name} created")
        return {
            "message": "Experience created successfully",
            "created_experience": new_experience,
        }
    except SQLAlchemyError as e:
        db.rollback()
        api_logger.error(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the experience"
        )


async def update_experience(
    experience_id: int,
    experience: ExperienceSchema,
    db: Session = Depends(database.get_db_session),
) -> dict:
    """Update an existing experience in the database.

    Args:
        experience_id (int): The ID of the experience to update.
        experience (ExperienceSchema): The experience to update.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message "Experience updated successfully" and the updated experience.
    """
    try:
        experience_to_update = await get_experience_by_id(experience_id, db)
        if not experience_to_update:
            api_logger.error(f"Experience {experience_id} not found")
            raise HTTPException(status_code=404, detail="Experience not found")

        for key, value in experience.model_dump(exclude_unset=True).items():
            setattr(experience_to_update, key, value)

        db.commit()
        db.refresh(experience_to_update)
        api_logger.info(f"Experience {experience_to_update.company_name} updated")
        return {
            "message": "Experience updated successfully",
            "updated_experience": experience_to_update,
        }
    except SQLAlchemyError as e:
        db.rollback()
        api_logger.error(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the experience"
        )


async def delete_experience(
    experience_id: int, db: Session = Depends(database.get_db_session)
) -> dict:
    """Delete an existing experience from the database.

    Args:
        experience_id (int): The ID of the experience to delete.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message "Experience deleted successfully" and the deleted experience.
            If the experience does not exist, the message will be "Experience not found" and the deleted_experience will be None.
    """
    try:
        experience_to_delete = await get_experience_by_id(experience_id, db)
        if not experience_to_delete:
            api_logger.error(f"Experience {experience_id} not found")
            return {"message": "Experience not found", "deleted_experience": None}

        db.delete(experience_to_delete)
        db.commit()
        api_logger.info(f"Experience {experience_to_delete.company_name} deleted")
        return {
            "message": "Experience deleted successfully",
            "deleted_experience": experience_to_delete,
        }
    except SQLAlchemyError as e:
        db.rollback()
        api_logger.error(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the experience"
        )
