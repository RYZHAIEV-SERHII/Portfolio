from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.security import get_current_user
from api.db import database
from api.schemas.experience import ExperienceSchema
from src.db.models import Experience, User


def get_all_experiences(db: Session = Depends(database.get_db_session)):
    """
    Retrieve all experiences
    """
    return db.query(Experience).all()


async def get_experience_by_id(
    experience_id: int, db: Session = Depends(database.get_db_session)
):
    """Retrieve an experience by ID"""
    return db.query(Experience).filter(Experience.id == experience_id).first()


async def create_experience(db: Session, experience: ExperienceSchema):
    """Create a new experience"""
    db_experience = Experience(
        user_id=experience.user_id,
        company_name=experience.company_name,
        role=experience.role,
        start_date=experience.start_date,
        end_date=experience.end_date,
        description=experience.description,
    )
    database.session.add(db_experience)
    database.session.commit()
    database.session.refresh(db_experience)
    return db_experience


# FIXME: make work
async def update_experience(
    experience_id: int,
    experience: ExperienceSchema,
    db: Session = Depends(database.get_db_session),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Update an existing experience with authentication and authorization"""
    try:
        db_experience = (
            db.query(Experience).filter(Experience.id == experience_id).first()
        )
        for key, value in experience.dict(exclude_unset=True).items():
            setattr(db_experience, key, value)

        db.commit()
        db.refresh(db_experience)
        return {"success": True, "data": db_experience}
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the experience"
        )


# FIXME: make work
async def delete_experience(
    experience_id: int, db: Session = Depends(database.get_db_session)
):
    """Delete an experience"""
    db_experience = await get_experience_by_id(experience_id, db)
    if not db_experience:
        return None
    database.session.delete(db_experience)
    database.session.commit()
    return db_experience
