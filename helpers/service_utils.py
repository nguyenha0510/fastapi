from config import config
from error_code import ERROR_CODE


def generate_log_msg(current_user, obj_target, req_content, start_time, res_msg, res_status=1):

    response = res_msg

    if isinstance(res_msg, int) and res_msg in ERROR_CODE.keys():
        response = ERROR_CODE[res_msg]

    return {
        'service_code': config['PROJECT_NAME'],
        'current_user': current_user,
        'object': obj_target,
        'request_content': req_content,
        'response_stt': res_status,
        'res_msg': response,
        'start_time': start_time
    }


def generate_response_example(example, error_codes=None):
    if error_codes is None:
        error_codes = []
    responses = {
        200: {
            "description": "Response from server",
            "content": {
                "application/json": {
                    "example": example
                }
            }
        }
    }

    for code in error_codes:
        if code in ERROR_CODE.keys():
            responses[code] = {
                "content": {
                    "application/json": {
                        "example": ERROR_CODE[code]
                    }
                }
            }

    return responses
