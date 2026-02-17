from fastapi import APIRouter, Depends
from b_e.helpers.security_jwt.security_jwt import decode_cookie

router = APIRouter()
# router.include_router(pp_ti_report.router, tags=["PP Reports"], prefix="/pp/report", dependencies=[Depends(check_actor_pp)])
# router.include_router(ti_report.router, tags=["Reports"], prefix="/report", dependencies=[Depends(decode_cookie)])

