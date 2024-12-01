from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# from api.security import check_authorization
from api.crud.experience import (
    get_all_experiences,
    get_experience_by_id,
    create_experience,
    update_experience,
    delete_experience,
)
from api.db import database
from api.schemas.experience import (
    ExperienceSchema,
    UpdateExperienceResponse,
    CreateExperienceResponse,
    DeleteExperienceResponse,
)

# from src.db.models import Experience

router = APIRouter(tags=["Experiences"])


@router.get("/experiences", response_model=List[ExperienceSchema])
async def list_experiences(db: Session = Depends(database.get_db_session)):
    """Retrieve all experiences"""
    experiences = get_all_experiences(db)
    return experiences


@router.get("/experiences/{experience_id}", response_model=ExperienceSchema)
async def get_experience(
    experience_id: int, db: Session = Depends(database.get_db_session)
):
    """Retrieve an experience by ID"""
    experience = await get_experience_by_id(experience_id, db)
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    return experience


# TODO: add authorization
@router.post("/experiences", response_model=CreateExperienceResponse)
async def create_new_experience(
    experience: ExperienceSchema, db: Session = Depends(database.get_db_session)
):
    """Create a new experience"""
    new_experience = await create_experience(experience, db)
    return new_experience


# TODO: add authorization
@router.put("/experiences/{experience_id}", response_model=UpdateExperienceResponse)
# @check_authorization(Experience, resource_id_attr="id", user_id_attr="user_id")
async def update_existing_experience(
    experience_id: int,
    experience: ExperienceSchema,
    db: Session = Depends(database.get_db_session),
):
    """Update an existing experience"""
    updated_experience = await update_experience(experience_id, experience, db)
    if not updated_experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    return updated_experience


# TODO: add authorization
@router.delete("/experiences/{experience_id}", response_model=DeleteExperienceResponse)
async def delete_existing_experience(
    experience_id: int, db: Session = Depends(database.get_db_session)
):
    """Delete an experience"""
    return await delete_experience(experience_id, db)
