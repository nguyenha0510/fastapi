from fastapi import APIRouter, Depends

from b_e.app.controllers import get_public_key
from b_e.helpers.security_jwt.security_jwt import decode_and_verify_cookie

router = APIRouter()
router.include_router(get_public_key.router, tags=["Public Key"], prefix="/public-key")
# router.include_router(pp_ti_report.router, tags=["PP Reports"], prefix="/pp/report", dependencies=[Depends(check_actor_pp)])
# router.include_router(ti_report.router, tags=["Reports"], prefix="/report", dependencies=[Depends(decode_cookie)])

