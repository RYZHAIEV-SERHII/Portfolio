from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from api.db import database
from api.schemas.skill import SkillSchema
from logging_setup import api_logger
from src.db.models import Skill


async def get_all_skills(db: Session = Depends(database.get_db_session)):
    """
    Retrieve all skills from the database.

    Returns:
        List[Skill]: A list of all skills stored in the database.
    """
    skills = db.query(Skill).all()
    api_logger.info("Skills. Status: retrieved")
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
    skill = db.query(Skill).get(skill_id)
    if not skill:
        api_logger.error(f"Skill {skill_id} not found")
        raise HTTPException(status_code=404, detail="Skill not found")
    api_logger.info(f"Skill {skill.skill_name} retrieved")
    return skill


async def get_skills_by_category(
    skill_category_id: int, db: Session = Depends(database.get_db_session)
):
    """
    Retrieve all skills for a specific category.

    Args:
        skill_category_id (int): The ID of the skill category to filter by.
        db (Session): The database session.

    Returns:
        List[Skill]: A list of skills belonging to the specified category.
    """
    skills = db.query(Skill).filter_by(skill_category_id=skill_category_id).all()
    api_logger.info(f"Skills in category {skill_category_id}. Status: retrieved")
    return skills


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
        new_skill = Skill(
            user_id=skill.user_id,
            skill_category_id=skill.skill_category_id,
            skill_name=skill.skill_name,
            proficiency_level=skill.proficiency_level,
        )
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)
        api_logger.info(f"Skill {new_skill.skill_name} created")
        return {
            "message": "Skill created successfully",
            "created_skill": new_skill,
        }
    except SQLAlchemyError as e:
        db.rollback()
        api_logger.error(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the skill"
        )


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

    try:
        skill_to_update = await get_skill_by_id(skill_id, db)
        if not skill_to_update:
            api_logger.error(f"Skill {skill_id} not found")
            raise HTTPException(status_code=404, detail="Skill not found")

        # Exclude nested relationships and unset values from the update
        update_data = skill.model_dump(exclude={"skill_category"}, exclude_unset=True)

        for key, value in update_data.items():
            setattr(skill_to_update, key, value)

        db.commit()
        db.refresh(skill_to_update)
        api_logger.info(f"Skill {skill_to_update.skill_name} updated")
        return {
            "message": "Skill updated successfully",
            "updated_skill": skill_to_update,
        }
    except SQLAlchemyError as e:
        db.rollback()
        api_logger.error(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the skill"
        )


async def delete_skill(
    skill_id: int, db: Session = Depends(database.get_db_session)
) -> dict:
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

    try:
        skill_to_delete = (
            db.query(Skill).options(joinedload(Skill.skill_category)).get(skill_id)
        )
        if not skill_to_delete:
            api_logger.error(f"Skill {skill_id} not found")
            return {"message": "Skill not found", "deleted_skill": None}

        db.delete(skill_to_delete)
        db.commit()
        api_logger.info(f"Skill {skill_to_delete.skill_name} deleted")
        return {
            "message": "Skill deleted successfully",
            "deleted_skill": skill_to_delete,
        }
    except SQLAlchemyError as e:
        db.rollback()
        api_logger.error(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the skill"
        )
