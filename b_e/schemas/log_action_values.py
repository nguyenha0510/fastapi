
from enum import Enum


class LogActionValuesEnum(str, Enum):
    post = "post"
    get = "get"
    put = "put"
    add = "add"
    view = "view"
    update = "update"
    delete = "delete"
