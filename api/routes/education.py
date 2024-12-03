from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.crud.education import (
    get_education_info,
    get_all_certifications,
    get_certification_by_id,
    create_certification,
    update_certification,
    delete_certification,
)
from api.db import database
from api.schemas.education import (
    EducationInfoResponse,
    CertificationInfoResponse,
    CreateCertificationResponse,
    UpdateCertificationResponse,
    DeleteCertificationResponse,
)

router = APIRouter(tags=["Education"])


@router.get("/education", response_model=EducationInfoResponse)
async def get_education():
    """Get education info"""
    return await get_education_info()


@router.get("/certifications", response_model=list[CertificationInfoResponse])
async def list_certifications(db: Session = Depends(database.get_db_session)):
    """Retrieve all certifications"""
    return await get_all_certifications(db)


@router.get(
    "/certifications/{certification_id}", response_model=CertificationInfoResponse
)
async def get_certification(
    certification_id: int, db: Session = Depends(database.get_db_session)
):
    """Retrieve a certification by ID"""
    certification = await get_certification_by_id(certification_id, db)
    if not certification:
        raise HTTPException(status_code=404, detail="Certification not found")
    return certification


@router.post("/certifications", response_model=CreateCertificationResponse)
async def create_new_certification(
    certification: CertificationInfoResponse,
    db: Session = Depends(database.get_db_session),
):
    """Create a new certification"""
    return await create_certification(certification, db)


@router.put(
    "/certifications/{certification_id}", response_model=UpdateCertificationResponse
)
async def update_certification_details(
    certification_id: int,
    certification: CertificationInfoResponse,
    db: Session = Depends(database.get_db_session),
):
    """Update an existing certification"""
    return await update_certification(certification_id, certification, db)


@router.delete(
    "/certifications/{certification_id}", response_model=DeleteCertificationResponse
)
async def delete_certification_by_id(
    certification_id: int, db: Session = Depends(database.get_db_session)
):
    """Delete a certification"""
    return await delete_certification(certification_id, db)
