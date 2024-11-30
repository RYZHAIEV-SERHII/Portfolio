from fastapi import APIRouter

from api.schemas.about import AboutInfoResponse, AboutInterestsResponse
from api.crud.about import get_all_interests, get_about_info

router = APIRouter(tags=["About"])


@router.get("/about", response_model=AboutInfoResponse)
async def about_info() -> AboutInfoResponse:
    """
    Retrieve the about me information.
    """
    return await get_about_info()


@router.get("/interests", response_model=AboutInterestsResponse)
async def get_interests() -> AboutInterestsResponse:
    """
    Retrieve the list of interests.
    """
    return await get_all_interests()
