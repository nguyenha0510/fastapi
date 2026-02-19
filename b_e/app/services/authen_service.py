from b_e.helpers.security_jwt.security_jwt import decrypt_with_private_key
from argon2 import PasswordHasher, exceptions
from argon2.profiles import RFC_9106_LOW_MEMORY, RFC_9106_HIGH_MEMORY

ph = PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY)


def verify_login_info(username: str, password: str):
    try:
        decode_username = decrypt_with_private_key(username)
        decode_password = decrypt_with_private_key(password)

        # if ph.verify(decode_password, username):

    except Exception:
        return False
    return True


def hash_password(password: str) -> str:
    return ph.hash(password)