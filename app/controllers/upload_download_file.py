import shutil
import os
from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from config import config
from app.services.attachment_service import *
from app.services.ti_report_service import *

router = APIRouter()


@router.post("/upload-file", response_description="Upload file")
async def upload_file(files: List[UploadFile], parent_id: str):
    report = await get_one_report(parent_id)
    if not report:
        return {
            "status_code": 404,
            "detail": [],
            "message": "There are no TiReport with an _id matching parent_id!!!",
            "success": False
        }
    else:
        file_upload_success = []
        directory = f"{config.get('FOLDER_STORE_FILE')}/{parent_id}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        for file in files:
            check_file_exited = f'{directory}/{file.filename}'
            if not os.path.exists(check_file_exited):
                with open(f'{directory}/{file.filename}', "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                attachment = Attachment(parent_id=parent_id, file_name=file.filename,
                                        file_size=os.path.getsize(f'{directory}/{file.filename}'),
                                        author=report.creator, url=f'{directory}/{file.filename}')
                new_attachment = await add_attachment(attachment)
                if new_attachment:
                    file_upload_success.append(file.filename)
                    pass
                else:
                    return {
                        "status_code": 404,
                        "detail": [],
                        "message": "Create attachment with file {} False!!!".format(file.filename),
                        "success": False
                    }
            else:
                continue
        return {
            "status_code": 200,
            "detail": [file for file in file_upload_success],
            "message": "Upload file success!!!",
            "success": True
        }


@router.post("/delete-file", response_description="Delete file")
async def delete_file(files_name: str):
    if not f"{config.get('FOLDER_STORE_FILE')}/{files_name}":
        return {
            "status_code": 404,
            "detail": None,
            "message": "Delete file export fail!!!",
            "success": False
        }
    else:
        os.unlink(f"{config.get('FOLDER_STORE_FILE')}/{files_name}")
        return {
            "status_code": 200,
            "detail": None,
            "message": "Delete file export success!!!",
            "success": True
        }


async def download(file_path):
    if os.path.isfile(file_path):
        return FileResponse(path=file_path)
    return None
