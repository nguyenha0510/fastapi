import jwt
from config import config, log
import datetime
from helpers.exceptions import Unauthorized


def encode_jwt(payload):
    private_key = config['GATEKEEPER_PRIVATE_KEY']
    encoded = jwt.encode(payload, private_key.encode(), algorithm='RS256')
    return encoded


def generate_access_token(scopes, name):
    token = {
        'type': 'access_token',
        'scope': scopes,
        'sub': name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=config['TOKEN_EXP_TIME']),
        'aud': config['AUD_JWT_NAME_FOR_VALIDATION']
    }
    token = encode_jwt(token)
    return token


def decode_token(token) -> dict:
    public_key = config['GATEKEEPER_PUBLIC_KEY']

    try:
        data = jwt.decode(token, public_key.encode(), algorithms='RS256', audience=config['AUD_JWT_NAME_FOR_VALIDATION'])
    except jwt.exceptions.InvalidSignatureError as e:
        raise Unauthorized(error_code=4011000)
    except jwt.exceptions.InvalidAudienceError as e:
        raise Unauthorized(error_code=4011001)
    except jwt.exceptions.ExpiredSignatureError as e:
        raise Unauthorized(error_code=4011002)
    except jwt.exceptions.DecodeError as e:
        raise Unauthorized(error_code=4011003)
    except Exception as e:
        log.error(str(e))
        raise Unauthorized()
    return data


def validate_scope(required_scopes, token):
    if len(required_scopes) == 0:
        return True

    req_scope = required_scopes[0].strip()

    if 'scope' in token.keys():
        scopes = token['scope'].split(" ")
        scope_set = set(scopes)
        if req_scope not in scope_set:
            raise Unauthorized(error_code=4011006)
    else:
        raise Unauthorized(error_code=4011007)

    return True
