from fastapi import Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
from helpers.security_jwt.security_jwt import decode_token, validate_scope
from helpers.exceptions import Unauthorized
from typing import Optional, Any
# from db_connector import db_session
# from models.db_models import User


# Don't touch this class unless you understand and know what you're doing

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            token = credentials.credentials

            if not credentials.scheme == "Bearer":
                raise Unauthorized(error_code=4011008)
            decode_token(token)
            return token
        else:
            raise Unauthorized(error_code=4011009)


authorize_method = JWTBearer()

"""
Function get_current_user

You can modify this function base on your need

Params Explanation:
- security_scopes.scopes is the scopes list that you declared in the controller
- token is the jwt string client use for this api 

How it works:
- Decode token to get the data from jwt string 
- Validate the scopes in data to see if the jwt has the scope needed for this api
    - You can also modify the validate_scope function at `./security_jwt.py` to your liking
- Find current user base on the info in data
- Init current user object (just a dict, you can modify this object to put more info of current user)
- Return current user
"""


# def get_current_user(
#         security_scopes: SecurityScopes,
#         token: Optional[str] = Security(authorize_method)
# ) -> Any:
#     data = decode_token(token)
#
#     validate_scope(security_scopes.scopes, data)
#
#     try:
#         username = data['sub']
#         current_user = {}
#         user = db_session.query(User).filter_by(username=username).first()
#         if user:
#             current_user['id'] = user.id
#             current_user['name'] = username
#             current_user['scope'] = data['scope']
#         else:
#             raise Unauthorized(error_code=4011005)
#     except Unauthorized as e:
#         raise Unauthorized(error_code=4011005)
#     except Exception as e:
#         raise Unauthorized(error_code=4011009)
#
#     return current_user
