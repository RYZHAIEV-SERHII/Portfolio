from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.db import database
from api.schemas.experience import ExperienceSchema
from src.db.models import Experience


def get_all_experiences(db: Session = Depends(database.get_db_session)):
    """
    Retrieve all experiences from the database.
    """
    return db.query(Experience).all()


async def get_experience_by_id(
    experience_id: int, db: Session = Depends(database.get_db_session)
):
    """Retrieve an experience by ID"""
    return db.query(Experience).filter(Experience.id == experience_id).first()


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
    db_experience = Experience(
        user_id=experience.user_id,
        company_name=experience.company_name,
        role=experience.role,
        start_date=experience.start_date,
        end_date=experience.end_date,
        description=experience.description,
    )
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return {
        "message": "Experience created successfully",
        "created_experience": db_experience,
    }


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
        db_experience = (
            db.query(Experience).filter(Experience.id == experience_id).first()
        )

        for key, value in experience.model_dump(exclude_unset=True).items():
            setattr(db_experience, key, value)

        db.commit()
        db.refresh(db_experience)
        return {
            "message": "Experience updated successfully",
            "updated_experience": db_experience,
        }
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemyError occurred: {e}")
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
    db_experience = await get_experience_by_id(experience_id, db)
    if not db_experience:
        return {"message": "Experience not found", "deleted_experience": None}
    db.delete(db_experience)
    db.commit()
    return {
        "message": "Experience deleted successfully",
        "deleted_experience": db_experience,
    }
