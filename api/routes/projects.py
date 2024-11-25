from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.crud.project import (
    get_all_projects,
    get_project_by_id,
    create_project,
    update_project,
    delete_project,
)
from api.schemas.project import ProjectSchema
from api.db import database

router = APIRouter(tags=["Projects"])


@router.get("/projects", response_model=List[ProjectSchema])
async def list_projects(db: Session = Depends(database.get_db_session)):
    """Retrieve all projects"""
    projects = await get_all_projects(db)
    return projects


@router.get("/projects/{project_id}", response_model=ProjectSchema)
async def get_project_details(
    project_id: int, db: Session = Depends(database.get_db_session)
):
    """Retrieve details of a specific project by its ID"""
    project = await get_project_by_id(project_id, db)
    return project


# TODO: Add authorization
# FIXME: make endpoint work
@router.post("/projects", response_model=ProjectSchema)
async def create_new_project(
    project: ProjectSchema, db: Session = Depends(database.get_db_session)
):
    """Create a new project"""
    new_project = await create_project(project, db)
    return new_project


# TODO: Add authorization
# FIXME: make endpoint work
@router.put("/projects/{project_id}", response_model=ProjectSchema)
async def update_project_details(
    project_id: int,
    project: ProjectSchema,
    db: Session = Depends(database.get_db_session),
):
    """Update details of an existing project"""
    updated_project = await update_project(project_id, project, db)
    return updated_project


# TODO: Add authorization
# FIXME: make endpoint work
@router.delete("/projects/{project_id}")
async def delete_project_by_id(
    project_id: int, db: Session = Depends(database.get_db_session)
):
    """Delete a project by its ID"""
    await delete_project(project_id, db)
    return JSONResponse(content={"message": "Project deleted"}, status_code=200)
