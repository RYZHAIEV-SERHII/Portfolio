from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.db import database
from api.schemas.skill import SkillSchema
from src.db.models import Skill


async def get_all_skills(db: Session = Depends(database.get_db_session)):
    """
    Retrieve all skills from the database.

    Returns:
        List[Skill]: A list of all skills stored in the database.
    """
    skills = db.query(Skill).all()
    return skills


async def get_skill_by_id(
    skill_id: int, db: Session = Depends(database.get_db_session)
):
    """
    Retrieve a specific skill by its ID.

    Args:
        skill_id (int): The ID of the skill to retrieve.
        db (Session): The database session.

    Returns:
        Skill: The skill instance.

    Raises:
        HTTPException: If the skill is not found.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


async def create_skill(
    skill: SkillSchema, db: Session = Depends(database.get_db_session)
):
    """
    Create a new skill in the database.

    Args:
        skill (SkillSchema): The skill data to create.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message "Skill created successfully" and the created skill instance.

    Raises:
        HTTPException: If the skill cannot be created.
    """
    try:
        new_skill = Skill(**skill.model_dump())
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)
        return {
            "message": "Skill created successfully",
            "created_skill": new_skill,
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail="Error creating skill: " + str(e))


async def update_skill(
    skill_id: int, skill: SkillSchema, db: Session = Depends(database.get_db_session)
):
    """
    Update a skill in the database.

    Args:
        skill_id (int): The id of the skill to update.
        skill (SkillSchema): The skill data to update.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message "Skill updated successfully" and the updated skill instance.

    Raises:
        HTTPException: If the skill is not found or cannot be updated.
    """
    skill_to_update = await get_skill_by_id(skill_id, db)
    if not skill_to_update:
        raise HTTPException(status_code=404, detail="Skill not found")
    try:
        for key, value in skill.model_dump().items():
            setattr(skill_to_update, key, value)
        db.commit()
        return {
            "message": "Skill updated successfully",
            "updated_skill": skill_to_update,
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail="Error updating skill: " + str(e))


async def delete_skill(skill_id: int, db: Session = Depends(database.get_db_session)):
    """
    Delete a skill in the database.

    Args:
        skill_id (int): The id of the skill to delete.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message "Skill deleted successfully" and the deleted skill instance.

    Raises:
        HTTPException: If the skill is not found or cannot be deleted.
    """
    skill_to_delete = await get_skill_by_id(skill_id, db)
    if not skill_to_delete:
        return {"message": "Skill not found", "deleted_skill": None}
    try:
        db.delete(skill_to_delete)
        db.commit()
        return {
            "message": "Skill deleted successfully",
            "deleted_skill": skill_to_delete,
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail="Error deleting skill: " + str(e))
