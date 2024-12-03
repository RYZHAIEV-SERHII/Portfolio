from datetime import date
from fastapi import Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.db import database
from api.schemas.education import (
    EducationInfoResponse,
    CertificationInfoResponse,
    CreateCertificationResponse,
    UpdateCertificationResponse,
    DeleteCertificationResponse,
)
from src.db.models import Certification


async def get_education_info():
    return EducationInfoResponse(
        institution_name="CyberBionic Systematics",
        degree="Python Developer",
        field_of_study="Information Technology",
        start_date=date(2024, 1, 11),
        end_date=date(2024, 8, 24),
        description="Specialized Python Developer Course focused on web development using Python, "
        "covering frameworks, databases, and deployment strategies.",
        relevant_coursework=[
            "Entertaining Chatbot",
            "Simple Telegram Bot",
            "Blog Platform",
        ],
        skills_acquired=[
            "Web Development",
            "Back-End Web Development",
            "API Development",
        ],
        diploma="https://testprovider.com/ua/search-certificate/tp22321258d",
    )


async def get_all_certifications(db: Session = Depends(database.get_db_session)):
    """Retrieve all certifications from the database."""
    return db.query(Certification).all()


async def get_certification_by_id(
    certification_id: int, db: Session = Depends(database.get_db_session)
):
    """Retrieve a certification by ID."""
    certification = db.query(Certification).get(certification_id)
    if not certification:
        raise HTTPException(status_code=404, detail="Certification not found")
    return certification


async def create_certification(
    certification: CertificationInfoResponse,
    db: Session = Depends(database.get_db_session),
) -> CreateCertificationResponse:
    """Create a new certification in the database."""
    try:
        new_certification = Certification(
            user_id=certification.user_id,
            name=certification.name,
            issuing_organization=certification.issuing_organization,
            issue_date=certification.issue_date,
            credential_id=certification.credential_id,
            credential_url=certification.credential_url,
            skills_acquired=", ".join(
                certification.skills_acquired or []
            ),  # Assuming skills_acquired is a list
        )
        db.add(new_certification)
        db.commit()
        db.refresh(new_certification)
        return CreateCertificationResponse(
            message="Certification created successfully",
            created_certification=new_certification,
        )
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the certification"
        )


async def update_certification(
    certification_id: int,
    certification: CertificationInfoResponse,
    db: Session = Depends(database.get_db_session),
) -> UpdateCertificationResponse:
    """Update an existing certification in the database."""
    try:
        certification_to_update = await get_certification_by_id(certification_id, db)
        if not certification_to_update:
            raise HTTPException(status_code=404, detail="Certification not found")

        for key, value in certification.model_dump(exclude_unset=True).items():
            if key == "skills_acquired":
                value = ", ".join(value or [])
            setattr(certification_to_update, key, value)

        db.commit()
        db.refresh(certification_to_update)
        return UpdateCertificationResponse(
            message="Certification updated successfully",
            updated_certification=certification_to_update,
        )
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the certification"
        )


async def delete_certification(
    certification_id: int, db: Session = Depends(database.get_db_session)
) -> DeleteCertificationResponse:
    """Delete an existing certification from the database."""
    try:
        certification_to_delete = await get_certification_by_id(certification_id, db)
        if not certification_to_delete:
            return DeleteCertificationResponse(
                message="Certification not found", deleted_certification=None
            )

        db.delete(certification_to_delete)
        db.commit()
        return DeleteCertificationResponse(
            message="Certification deleted successfully",
            deleted_certification=certification_to_delete,
        )
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemyError occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the certification"
        )
