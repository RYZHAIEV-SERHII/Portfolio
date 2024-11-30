from fastapi import APIRouter

from api.crud.contact import get_contact_info
from api.schemas.contact import ContactInfoResponse

router = APIRouter(tags=["Contact"])


@router.get("/contact", response_model=ContactInfoResponse)
async def contact_info() -> ContactInfoResponse:
    """
    Retrieve the contact information.
    """
    return await get_contact_info()
