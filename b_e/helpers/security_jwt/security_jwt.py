import jwt
from fastapi import Request, HTTPException, status
from b_e.config import config


def decode_cookie(request: Request):
    cookie = request.headers.get('cookie')
    # cookie = config.get('DEFAULT_COOKIE')
    if not cookie:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    else:
        list_value_creator = cookie.split("; ")
        if not any(value.startswith('access_token_cookie') for value in cookie.split("; ")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            for value in list_value_creator:
                if value.startswith('access_token_cookie'):
                    access_token = value.split('access_token_cookie=')
                    actor = jwt.decode(access_token[1], key=None, options={"verify_signature": False})
                    if actor.get('preferred_username'):
                        request.state.current_user = actor.get('preferred_username')
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                        )
