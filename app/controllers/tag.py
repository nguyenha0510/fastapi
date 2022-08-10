from fastapi import APIRouter, Body
from app.services.tag_service import *
from models.tag import *

router = APIRouter()


@router.get("/get_all_tag", response_description="Tag data search from the database", response_model=Response)
async def get_all_tags():
    all_tags = await get_all_tag()
    if all_tags:
        return {
            "status_code": 200,
            "detail": all_tags,
            "message": "Search all success",
            "success": True
        }
    return {
        "status_code": 404,
        "message": "Search all report fail",
        "success": False
    }


@router.post("/add_tag", response_description="Tag data added into the database", response_model=Response)
async def add_tag_data(tag: Tag = Body(...)):
    print(tag)
    print(type(tag))
    new_tag = await add_tag(tag)
    if new_tag:
        return {
            "status_code": 200,
            "detail": new_tag,
            "message": "Tag created successfully",
            "success": True
        }
    return {
        "status_code": 200,
        "detail": [],
        "message": "Error",
        "success": False
    }
