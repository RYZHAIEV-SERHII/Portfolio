from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.crud.skill import (
    get_all_skills,
    get_skill_by_id,
    get_skills_by_category,
    create_skill,
    update_skill,
    delete_skill,
)
from api.db import database
from api.schemas.skill import (
    SkillSchema,
    CreateSkillResponse,
    DeleteSkillResponse,
    UpdateSkillResponse,
)

router = APIRouter(tags=["Skills"])


@router.get("/skills", response_model=List[SkillSchema])
async def list_skills(db: Session = Depends(database.get_db_session)):
    """Retrieve all skills"""
    skills = await get_all_skills(db)
    return skills


@router.get("/skills/{skill_id}", response_model=SkillSchema)
async def get_skill(skill_id: int, db: Session = Depends(database.get_db_session)):
    """Retrieve details of a specific skill by its ID"""
    skill = await get_skill_by_id(skill_id, db)
    return skill


@router.get("/skills/category/{skill_category_id}", response_model=List[SkillSchema])
async def get_skills_sorted_by_category(
    skill_category_id: int, db: Session = Depends(database.get_db_session)
):
    """Retrieve skills by category ID"""
    skills = await get_skills_by_category(skill_category_id, db)
    return skills


@router.post("/skills", response_model=CreateSkillResponse)
async def create_new_skill(
    skill: SkillSchema, db: Session = Depends(database.get_db_session)
):
    """Create a new skill"""
    new_skill = await create_skill(skill, db)
    return new_skill


@router.put("/skills/{skill_id}", response_model=UpdateSkillResponse)
async def update_skill_details(
    skill_id: int, skill: SkillSchema, db: Session = Depends(database.get_db_session)
):
    """Update an existing skill"""
    updated_skill = await update_skill(skill_id, skill, db)
    return updated_skill


@router.delete("/skills/{skill_id}", response_model=DeleteSkillResponse)
async def delete_skill_by_id(
    skill_id: int, db: Session = Depends(database.get_db_session)
):
    """Delete a skill"""
    deleted_skill = await delete_skill(skill_id, db)
    return deleted_skill
