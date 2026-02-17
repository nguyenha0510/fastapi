from b_e.helpers.utilities.http_response import http_json_response
from b_e.helpers.utilities.pp_write_logs import log_api


def check_data_return(status_code, data_return, action, service_code, request):
    if status_code != 200:
        log_api(action=action,
                service_code=service_code,
                response_status='FAILED',
                response_content=(status_code, data_return),
                request=request)
        return http_json_response(status_code, message=data_return)

    log_api(action=action,
            service_code=service_code,
            response_status='SUCCESS',
            response_content=(status_code, data_return),
            request=request)
    return http_json_response(status_code, data_return)
