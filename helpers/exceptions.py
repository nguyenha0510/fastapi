from typing import Any, List
from error_code import ERROR_CODE
from fastapi import HTTPException


def get_error_msg(error_code, extra_info, *arg):
    if error_code not in ERROR_CODE:
        return None

    error_msg = ERROR_CODE[error_code]
    if 'message' in error_msg.keys():
        template_msg = error_msg['message']
        try:
            error_msg['message'] = template_msg.format(*arg)
        except IndexError:
            error_msg['message'] = template_msg
        
        if extra_info:
            error_msg['info'] = extra_info
    return error_msg


class ErrorException(HTTPException):
    status_code = 500

    def __init__(
            self,
            error_code: Any = None,
            error_args: List[Any] = [],
            error_info: Any = None
    ) -> None:
        if not error_code:
            error_code = self.status_code

        self.error_code = error_code

        detail = get_error_msg(error_code, error_info, *error_args)
        super().__init__(status_code=self.status_code, detail=detail)


class Unauthorized(ErrorException):
    status_code = 401


class NotAcceptable(ErrorException):
    status_code = 406


class BadRequest(ErrorException):
    status_code = 400


class Forbidden(ErrorException):
    status_code = 403


class NotFound(ErrorException):
    status_code = 404


class APIError(ErrorException):

    def __init__(
            self,
            status_code: int = 500,
            error_code: Any = None,
            error_args: List[Any] = [],
            error_info: Any = None
    ) -> None:
        self.status_code = status_code
        super().__init__(error_code, error_args, error_info)
