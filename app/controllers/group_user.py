from fastapi import APIRouter
from app.services.group_user_service import *

router = APIRouter()


@router.get("/search", response_description="Group User data search from the database")
async def get_all_group():
    all_group = await retrieve_all_group_user()
    if all_group:
        return {
            "status_code": 200,
            "detail": all_group,
            "message": "Search all success",
            "success": True
        }
    return {
        "status_code": 404,
        "message": "DO not have any group valid!!!",
        "success": False
    }
