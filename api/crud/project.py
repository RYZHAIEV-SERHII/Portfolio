from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from api.db import database
from api.schemas.project import ProjectSchema
from logging_setup import api_logger
from src.db.models import Project


async def get_all_projects(db: Session):
    """
    Retrieve all projects from the database.

    Returns:
        list: A list of all projects.
    """
    api_logger.info("Projects. Status: retrieved")
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
        api_logger.error(f"Project {project_id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    api_logger.info(f"Project {project.title} retrieved")
    return project


async def create_project(
    project: ProjectSchema, user_id: int, db: Session = Depends(database.get_db_session)
) -> dict:
    """
    Create a new project in the database.

    Args:
        project (ProjectSchema): The project data to create.
        user_id (int): The ID of the user who created the project.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message "Project created successfully" and the created project instance.

    """
    try:
        new_project = Project(
            user_id=user_id,  # Use the current user's ID
            title=project.title,
            description=project.description,
            tech_stack=project.tech_stack,
            url=project.url,
            project_category_id=project.project_category_id,
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        api_logger.info(f"Project {new_project.title} created")
        return {
            "message": "Project created successfully",
            "created_project": new_project,
        }
    except SQLAlchemyError as e:
        db.rollback()
        api_logger.error(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the project"
        )


async def update_project(
    project_id: int,
    project: ProjectSchema,
    user_id: int,
    db: Session = Depends(database.get_db_session),
) -> dict:
    """
    Update an existing project in the database.

    Args:
        project_id (int): The ID of the project to update.
        project (ProjectSchema): The updated project data.
        user_id (int): The ID of the user who is updating the project.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message "Project updated successfully" and the updated project instance.
    """
    try:
        project_to_update = await get_project_by_id(project_id, db)
        if not project_to_update:
            api_logger.error(f"Project {project_id} not found")
            raise HTTPException(status_code=404, detail="Project not found")

        # Ensure the project belongs to the current user
        if project_to_update.user_id != user_id:
            api_logger.error("Not authorized to update this project")
            raise HTTPException(
                status_code=403, detail="Not authorized to update this project"
            )

        # Exclude nested relationships and unset values from the update
        update_data = project.model_dump(
            exclude={"project_category", "images"}, exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(project_to_update, key, value)

        db.commit()
        db.refresh(project_to_update)
        api_logger.info(f"Project {project_to_update.title} updated")
        return {
            "message": "Project updated successfully",
            "updated_project": project_to_update,
        }
    except SQLAlchemyError as e:
        db.rollback()
        api_logger.error(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the project"
        )


async def delete_project(
    project_id: int, user_id: int, db: Session = Depends(database.get_db_session)
) -> dict:
    """
    Delete a project from the database.

    Args:
        project_id (int): The ID of the project to delete.
        user_id (int): The ID of the user who is deleting the project.
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
            api_logger.error(f"Project {project_id} not found")
            return {"message": "Project not found", "deleted_project": None}

        # Ensure the project belongs to the current user
        if db_project.user_id != user_id:
            api_logger.error("Not authorized to delete this project")
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this project"
            )

        db.delete(db_project)
        db.commit()
        api_logger.info(f"Project {db_project.title} deleted")
        return {
            "message": "Project deleted successfully",
            "deleted_project": db_project,
        }
    except SQLAlchemyError as e:
        db.rollback()
        api_logger.error(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the project"
        )
