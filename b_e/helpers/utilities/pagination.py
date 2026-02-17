import math
from b_e.helpers.constant.pagination import MAX_RESULTS_PER_PAGE, RESULTS_PER_PAGE


def pagination(offset: int, size: int, total_document: int) -> dict:
    data_return = {}
    if 0 <= size <= RESULTS_PER_PAGE:
        size = RESULTS_PER_PAGE
    if size > MAX_RESULTS_PER_PAGE:
        size = MAX_RESULTS_PER_PAGE
    total_page = int(math.ceil(total_document / size))

    data_return["offset"] = offset
    data_return["size"] = size
    data_return["total_pages"] = total_page
    data_return["total_results"] = total_document
    return data_return


def check_offset_size(offset: int, size: int):
    result = {"offset": offset, "size": size}
    if offset >= 0 and 0 < size <= MAX_RESULTS_PER_PAGE:
        return result
    else:
        if offset < 0:
            offset = 0
        if size <= 0:
            size = RESULTS_PER_PAGE
        elif size > MAX_RESULTS_PER_PAGE:
            size = MAX_RESULTS_PER_PAGE
        result["offset"] = offset
        result["size"] = size
        return result

