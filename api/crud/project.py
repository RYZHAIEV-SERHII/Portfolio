from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from api.db import database
from api.schemas.project import ProjectSchema
from src.db.models import Project


async def get_all_projects(db: Session):
    """
    Retrieve all projects from the database.

    Returns:
        list: A list of all projects.
    """
    return db.query(Project).all()


async def get_project_by_id(
    project_id: int, db: Session = Depends(database.get_db_session)
) -> Project:
    """
    Retrieve a specific project by its ID.

    Args:
        project_id (int): The ID of the project to retrieve.
        db (Session): The database session.

    Returns:
        Project: The project instance.

    Raises:
        HTTPException: If the project is not found.
    """
    project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


async def create_project(
    project: ProjectSchema, db: Session = Depends(database.get_db_session)
) -> dict:
    """
    Create a new project in the database.

    Args:
        project (ProjectSchema): The project data to create.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message "Project created successfully" and the created project instance.

    """
    try:
        new_project = Project(
            user_id=project.user_id,
            title=project.title,
            description=project.description,
            tech_stack=project.tech_stack,
            url=project.url,
            project_category_id=project.project_category_id,
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return {
            "message": "Project created successfully",
            "created_project": new_project,
        }
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the project"
        )


async def update_project(
    project_id: int,
    project: ProjectSchema,
    db: Session = Depends(database.get_db_session),
) -> dict:
    """
    Update an existing project in the database.

    Args:
        project_id (int): The ID of the project to update.
        project (ProjectSchema): The updated project data.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message "Project updated successfully" and the updated project instance.
    """
    try:
        project_to_update = await get_project_by_id(project_id, db)
        if not project_to_update:
            raise HTTPException(status_code=404, detail="Project not found")

        # Exclude nested relationships and unset values from the update
        update_data = project.model_dump(
            exclude={"project_category", "images"}, exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(project_to_update, key, value)

        db.commit()
        db.refresh(project_to_update)
        return {
            "message": "Project updated successfully",
            "updated_project": project_to_update,
        }
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the project"
        )


async def delete_project(
    project_id: int, db: Session = Depends(database.get_db_session)
) -> dict:
    """
    Delete a project from the database.

    Args:
        project_id (int): The ID of the project to delete.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message "Project deleted successfully" and the deleted project.
            If the project does not exist, the message will be "Project not found" and the deleted_project will be None.
    """
    try:
        db_project = (
            db.query(Project)
            .options(joinedload(Project.project_category))
            .get(project_id)
        )
        if not db_project:
            return {"message": "Project not found", "deleted_project": None}

        db.delete(db_project)
        db.commit()
        return {
            "message": "Project deleted successfully",
            "deleted_project": db_project,
        }
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the project"
        )
