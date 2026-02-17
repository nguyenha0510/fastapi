import datetime
import uuid
import base64

from typing import Union
from fastapi import Request
import hashlib


def generate_request_id(request: Request, start_time: float, service_code: str):
    rq_uuid = uuid.uuid1()
    request_id = base64.b64encode(
        (str(start_time) + '-' + str(rq_uuid) + '-' + str(request.client.host) + '-' + service_code).encode(
            'utf-8'))
    return request_id


def generate_file_name(file_name: str):
    new_file_name = hashlib.sha1('{}'.format(file_name).encode('utf-8')).hexdigest()
    return new_file_name


async def generate_code(prefix: str, next_number: int):
    if next_number <= 9999:
        return prefix + str(datetime.datetime.now().year) + "_" + '{:0>4}'.format(str(next_number))
    else:
        return prefix + str(datetime.datetime.now().year) + "_" + str(next_number)

