import datetime

from b_e.config import config, log
from b_e.helpers.action_log import ActionLogger as action_logger


def log_api(action, service_code, response_status, response_content, request=None):
    return action_logger.info_log(self=action_logger(config, log),
                                  action=action,
                                  request=request,
                                  ApplicationCode='asset_api',
                                  ServiceCode=service_code,
                                  StartTime=datetime.datetime.now(),
                                  ResponseStatus=response_status,
                                  ResponseContent=response_content)
