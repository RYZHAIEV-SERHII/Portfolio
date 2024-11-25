from typing import List

from fastapi.params import Depends
from sqlalchemy.orm import Session

from fastapi import HTTPException

from api.db import database
from api.schemas.project import ProjectSchema
from src.db.models import Project


async def get_all_projects(db: Session) -> List[Project]:
    """
    Retrieve all projects from the database.

    Returns:
        list: A list of all projects.
    """
    projects = db.query(Project).all()
    return projects


async def get_project_by_id(
    project_id: int, db: Session = Depends(database.get_db_session)
) -> Project:
    """
    Retrieve a specific project by its ID.

    Args:
        project_id (int): The ID of the project to retrieve.

    Returns:
        Project: The project instance.

    Raises:
        HTTPException: If the project is not found.
    """
    project = db.query(Project).get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# FIXME: make endpoint work
async def create_project(project: ProjectSchema, db: Session) -> Project:
    """
    Create a new project in the database.

    Args:
        project (ProjectSchema): The project data to create.

    Returns:
        Project: The created project instance.
    """
    new_project = Project(
        user_id=project.user_id,
        title=project.title,
        description=project.description,
        tech_stack=project.tech_stack,
        url=project.url,
        project_category_id=project.project_category_id,
        images=project.images,
    )
    db.add(new_project)
    db.commit()
    return new_project


# FIXME: make endpoint work
async def update_project(
    project_id: int, project: ProjectSchema, db: Session
) -> Project:
    """
    Update an existing project in the database.

    Args:
        project_id (int): The ID of the project to update.
        project (ProjectSchema): The updated project data.

    Returns:
        Project: The updated project instance.
    """
    existing_project = db.query(Project).get(project_id)
    if existing_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    existing_project.user_id = project.user_id
    existing_project.title = project.title
    existing_project.description = project.description
    existing_project.tech_stack = project.tech_stack
    existing_project.url = project.url
    existing_project.project_category_id = project.project_category_id
    existing_project.images = project.images

    db.commit()
    return existing_project


# FIXME: make endpoint work
async def delete_project(project_id: int, db: Session) -> dict:
    """
    Delete a project from the database.

    Args:
        project_id (int): The ID of the project to delete.

    Returns:
        dict: A message indicating successful deletion.
    """
    existing_project = db.query(Project).get(project_id)
    if existing_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(existing_project)
    db.commit()
    return {"message": "Project deleted"}
