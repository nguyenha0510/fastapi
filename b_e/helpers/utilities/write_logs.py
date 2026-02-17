from b_e.helpers.action_log import ActionLogger as action_logger
from b_e.config import config, log
from b_e.schemas.log_action_values import LogActionValuesEnum


def log_api(request, request_content, response_content, request_id=None, actor='', start_time=None, end_time=None,
            method=LogActionValuesEnum, object_str=str, error_code=None, error_description=None):
    if actor == '':
        actor += "Not have cookie"
    if error_code is not None:
        return action_logger.info_log(self=action_logger(config, log),
                                      action=f'{method.value.upper()}',
                                      request=request,
                                      ApplicationCode=f'{object_str}_api',
                                      ServiceCode=f'{method}-{object_str}',
                                      Request_Id=request_id,
                                      RequestContent=request_content,
                                      StartTime=start_time,
                                      EndTime=end_time,
                                      ActionName=f'{method}-{object_str}',
                                      Object=object_str,
                                      UserName=actor,
                                      ResponseStatus='FALSE',
                                      ErrorCode=error_code,
                                      ErrorDescription=error_description)
    else:
        return action_logger.info_log(self=action_logger(config, log),
                                      action=f'{method.upper()}',
                                      request=request,
                                      ApplicationCode=f'{object_str}_api',
                                      ServiceCode=f'{method}-{object_str}',
                                      Request_Id=request_id,
                                      RequestContent=request_content,
                                      StartTime=start_time,
                                      EndTime=end_time,
                                      ActionName=f'{method}-{object_str}',
                                      Object=object_str,
                                      UserName=actor,
                                      ResponseStatus='TRUE',
                                      ResponseContent=response_content)


def log_service(method, request_content, start_time, end_time, actor, response_status, response_content: str,
                object_str=str):
    return action_logger.info_log_service(self=action_logger(config, log),
                                          action=method,
                                          ServiceCode=f"{method}-{object_str}-service",
                                          ActionName=f"{method}-{object_str}",
                                          StartTime=start_time,
                                          EndTime=end_time,
                                          UserName=actor,
                                          Object=object_str,
                                          request=request_content,
                                          ResponseStatus=response_status,
                                          ResponseContent=response_content)
