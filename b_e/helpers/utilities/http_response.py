from b_e.error_code import ERROR_CODE
from fastapi.responses import JSONResponse


def http_json_response(status_code=200, data_return=None, message=""):
    if data_return is None:
        data_return = {}
    if str(status_code).startswith('2'):
        if "data" in data_return:
            content = data_return
        else:
            content = {
                "data": data_return
            }
        return JSONResponse(status_code=status_code, content=content)
    else:
        if status_code not in ERROR_CODE:
            status_code = 400
        msg = ERROR_CODE[status_code].copy()
        if message != "":
            msg["message"] += ": " + message
        return JSONResponse(status_code=status_code, content=msg)
