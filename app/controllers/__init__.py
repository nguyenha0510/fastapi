from fastapi import APIRouter
from app.controllers import group_user, send_mail, statistical, tag, ti_report, upload_download_file

router = APIRouter()
router.include_router(ti_report.router, tags=["Reports"], prefix="/report")
router.include_router(statistical.router, tags=["Statistical"], prefix="/statistical")
router.include_router(upload_download_file.router, tags=["File"], prefix="/file")
router.include_router(tag.router, tags=["Tags"], prefix="/tag")
router.include_router(group_user.router, tags=["Groups"], prefix="/group")
router.include_router(send_mail.router, tags=["Email"], prefix="/mail")
