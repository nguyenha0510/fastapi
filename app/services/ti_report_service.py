import datetime
from typing import List, Union, Dict

from beanie import PydanticObjectId

from models.ti_report import TiReport, TiReportShortView, FilterReport, ActionReport

ti_report_collection = TiReport


async def add_ti_report(new_report: TiReport) -> TiReport:
    report = await new_report.create()
    if report:
        query_year = {"$expr": {"$eq": [{"$year": "$create_time"}, datetime.datetime.today().year]}}
        result_query_year = await ti_report_collection.find(query_year).count()
        new_value = {"$set": {"create_time": datetime.datetime.now(),
                              "code_report": "VTI_" + str(datetime.datetime.today().year) + "_" + str(
                                  result_query_year + 1),
                              "status": 1}}
        await report.update(new_value)
    return report


async def insert_ti_report(new_report: TiReport) -> TiReport:
    report = await new_report.insert()
    return report


async def retrieve_all_report() -> List[TiReport]:
    reports = await ti_report_collection.find({"active": True}).sort("-create_time").to_list()
    return reports


async def get_one_report(id: str) -> TiReport:
    obj_id = PydanticObjectId(id)
    report = await ti_report_collection.get(obj_id)
    return report


async def find_report(data_find: dict) -> List[TiReport]:
    data_find["active"] = True
    result = await ti_report_collection.find(data_find).to_list()
    if result:
        return result


async def update_one_report(id: PydanticObjectId, new_data: dict) -> bool:
    des_body = {k: v for k, v in new_data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    report = await ti_report_collection.find({"_id": id, "active": True}).to_list()
    if report:
        await report[0].update(update_query)
        return True
    return False


async def update_many_report(ids: List[PydanticObjectId], new_data: dict):
    for id in ids:
        report = ti_report_collection.find({"_id": id, "active": True}).to_list()
        if report:
            des_body = {k: v for k, v in new_data.items() if v is not None}
            update_query = {"$set": {
                field: value for field, value in des_body.items()
            }}
            await report[0].update(update_query)
    return True


async def search_report_by_filter(filter_dict: Union[FilterReport, ActionReport]) -> List[TiReport]:
    query = {"active": True}
    if filter_dict.keyword:
        query["title"] = {"$regex": filter_dict.keyword}
    if filter_dict.creator:
        query["creator"] = filter_dict.creator
    if filter_dict.tag:
        query["tag"] = {"$all": filter_dict.tag}
    if filter_dict.language:
        query["language"] = {"$in": filter_dict.language}
    if filter_dict.type:
        query["type"] = {"$all": filter_dict.type}
    if filter_dict.tlp:
        query["tlp"] = {"$in": filter_dict.tlp}
    if filter_dict.status:
        query["status"] = {"$in": filter_dict.status}
    if filter_dict.time:
        time_start = datetime.datetime.fromtimestamp((filter_dict.time["gte"]) / 1000)
        time_end = datetime.datetime.fromtimestamp((filter_dict.time["lte"] / 1000))
        query["create_time"] = {"$gte": time_start, "$lt": time_end}
    result = await ti_report_collection.find(query).sort("-create_time").skip(filter_dict.offset).limit(
        filter_dict.size).to_list()
    if result:
        return result


async def aggregate_report() -> List:
    result = await ti_report_collection.aggregate(
        [{
            "$group": {
                "_id": "$creator",
                "count": {"$sum": 1}
            }}
        ]).to_list()
    return result
