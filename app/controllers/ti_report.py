from fastapi import APIRouter, Body
from fastapi.responses import FileResponse
from app.services.ti_report_service import *
from app.services.tag_service import *
from app.services.history_service import *
from app.services.attachment_service import *
from models.ti_report import *
from models.attachment import *
from config import config

import base64
import yaml
import xlwt
import datetime
import os
import requests

router = APIRouter()


@router.post("/add_new", response_description="Report data added into the database", response_model=Response)
async def add_report_data(report: TiReport = Body(...)):
    if report.creator:
        creator = report.creator
        list_value_creator = creator.split(";")
        if len(list_value_creator) != 3:
            return {
                "status_code": 404,
                "detail": [],
                "message": "Creator must be cookie!",
                "success": False
            }
        else:
            access_token_cookie = list_value_creator[1].split("access_token_cookie=")
            if access_token_cookie:
                access_token = access_token_cookie[1].split(".")
                if len(access_token) != 3:
                    return {
                        "status_code": 404,
                        "detail": [],
                        "message": "Access token is invalid!",
                        "success": False
                    }
                else:
                    try:
                        decode_access_token = base64.b64decode(access_token[1])
                        yaml_value_access_token = yaml.load(decode_access_token)
                        if yaml_value_access_token['preferred_username']:
                            report.creator = yaml_value_access_token['preferred_username']
                            if report.tlp:
                                try:
                                    check = CheckTlpEnum(report.tlp)
                                except:
                                    return {
                                        "status_code": 404,
                                        "message": "Lỗi giá trị TLP",
                                        "success": False
                                    }
                            if report.type:
                                for value_type in report.type:
                                    try:
                                        check = CheckTypeEnum(value_type)
                                    except:
                                        return {
                                            "status_code": 404,
                                            "message": "Lỗi giá trị type",
                                            "success": False
                                        }
                            new_report = await add_ti_report(report)
                            if new_report:
                                del new_report.languages_parent_id
                                return {
                                    "status_code": 200,
                                    "detail": new_report,
                                    "message": "Report created successfully",
                                    "success": True
                                }
                            return {
                                "status_code": 404,
                                "detail": [],
                                "message": "Error",
                                "success": False
                            }
                        else:
                            return {
                                "status_code": 404,
                                "detail": [],
                                "message": "Not have preferred_username when decode access token",
                                "success": False
                            }
                    except:
                        return {
                            "status_code": 404,
                            "detail": [],
                            "message": "Cookie is invalid!",
                            "success": False
                        }
            else:
                return {
                    "status_code": 404,
                    "detail": [],
                    "message": "Cookie is invalid!",
                    "success": False
                }
    else:
        return {
            "status_code": 404,
            "detail": [],
            "message": "Creator must be not null!",
            "success": False
        }


@router.post("/delete", response_description="Report data deleted from the database")
async def inactive_report(report_ids: DeleteReport = Body(...)):
    if report_ids.cookie:
        cookie = report_ids.cookie
        list_value_cookie = cookie.split(";")
        if len(list_value_cookie) != 3:
            return {
                "status_code": 404,
                "detail": [],
                "message": "Cookie í invalid!",
                "success": False
            }
        else:
            access_token_cookie = list_value_cookie[1].split("access_token_cookie=")
            if access_token_cookie:
                access_token = access_token_cookie[1].split(".")
                if len(access_token) != 3:
                    return {
                        "status_code": 404,
                        "detail": [],
                        "message": "Access token is invalid!",
                        "success": False
                    }
                else:
                    try:
                        decode_access_token = base64.b64decode(access_token[1])
                        yaml_value_access_token = yaml.load(decode_access_token)
                        if yaml_value_access_token['preferred_username']:
                            report_ids.cookie = yaml_value_access_token['preferred_username']
                            delete = {"active": False}
                            deleted_report = await update_many_report(report_ids.reports_delete, delete)
                            if deleted_report:
                                return {
                                    "status_code": 200,
                                    "message": "Report with ID: {} removed".format(report_ids.reports_delete),
                                    "success": True
                                }
                            else:
                                return {
                                    "status_code": 404,
                                    "message": "Report with id {0} doesn't exist".format(report_ids.reports_delete),
                                    "success": False
                                }
                        else:
                            return {
                                "status_code": 404,
                                "detail": [],
                                "message": "Not have preferred_username when decode access token",
                                "success": False
                            }
                    except:
                        return {
                            "status_code": 404,
                            "detail": [],
                            "message": "Cookie is invalid!",
                            "success": False
                        }
            else:
                return {
                    "status_code": 404,
                    "detail": [],
                    "message": "Cookie is invalid!",
                    "success": False
                }
    else:
        return {
            "status_code": 404,
            "detail": [],
            "message": "Cookie must be not null!",
            "success": False
        }


@router.post("/mark", response_description="Report data marked from the database")
async def set_mark_report(report_id: MarkReport = Body(...)):
    if report_id.cookie:
        cookie = report_id.cookie
        list_value_cookie = cookie.split(";")
        if len(list_value_cookie) != 3:
            return {
                "status_code": 404,
                "detail": [],
                "message": "Creator must be cookie!",
                "success": False
            }
        else:
            access_token_cookie = list_value_cookie[1].split("access_token_cookie=")
            if access_token_cookie:
                access_token = access_token_cookie[1].split(".")
                if len(access_token) != 3:
                    return {
                        "status_code": 404,
                        "detail": [],
                        "message": "Access token is invalid!",
                        "success": False
                    }
                else:
                    try:
                        decode_access_token = base64.b64decode(access_token[1])
                        yaml_value_access_token = yaml.load(decode_access_token)
                        if yaml_value_access_token['preferred_username']:
                            report_id.cookie = yaml_value_access_token['preferred_username']
                            report = await get_one_report(report_id.report_mark)
                            if report:
                                mark = not report.mark
                                new_data = {"mark": mark}
                                report_mark = await update_one_report(report.id, new_data)
                                if report_mark:
                                    return {
                                        "status_code": 200,
                                        "message": "Report with ID: {} marked".format(report_id.report_mark),
                                        "success": True
                                    }
                                return {
                                    "status_code": 404,
                                    "message": "Report with id {0} doesn't exist".format(report_id.report_mark),
                                    "success": False
                                }
                            return {
                                "status_code": 404,
                                "message": "Report with id {0} doesn't exist".format(report_id.report_mark),
                                "success": False
                            }
                        else:
                            return {
                                "status_code": 404,
                                "detail": [],
                                "message": "Not have preferred_username when decode access token",
                                "success": False
                            }
                    except:
                        return {
                            "status_code": 404,
                            "detail": [],
                            "message": "Cookie is invalid!",
                            "success": False
                        }
            else:
                return {
                    "status_code": 404,
                    "detail": [],
                    "message": "Cookie is invalid!",
                    "success": False
                }
    else:
        return {
            "status_code": 404,
            "detail": [],
            "message": "Creator must be not null!",
            "success": False
        }


@router.get("/search", response_description="Report data search from the database", response_model=Response)
async def get_all_report():
    all_report = await retrieve_all_report()
    if all_report:
        return {
            "status_code": 200,
            "detail": all_report,
            "message": "Search all success",
            "success": True
        }
    return {
        "status_code": 404,
        "message": "Search all report fail",
        "success": False
    }


@router.post("/filter", response_description="Report data search from the database", response_model=Response)
async def filter_report(filter_dic: FilterReport = Body(...)):
    if filter_dic.tlp:
        for value_tlp in filter_dic.tlp:
            try:
                check = CheckTlpEnum(value_tlp)
            except:
                return {
                    "status_code": 404,
                    "message": "Lỗi giá trị TLP",
                    "success": False
                }
    if filter_dic.status:
        for value_status in filter_dic.status:
            try:
                check = StatusEnum(value_status)
            except:
                return {
                    "status_code": 404,
                    "message": "Lỗi giá trị status",
                    "success": False
                }
    if filter_dic.type:
        for value_type in filter_dic.type:
            try:
                check = CheckTypeEnum(value_type)
            except:
                return {
                    "status_code": 404,
                    "message": "Lỗi giá trị type",
                    "success": False
                }
    filter_all_reports = await search_report_by_filter(filter_dic)
    if filter_all_reports:
        for rec in filter_all_reports:
            del rec.languages_parent_id
        return {
            "status_code": 200,
            "detail": filter_all_reports,
            "message": "Search all success",
            "success": True
        }
    return {
        "status_code": 404,
        "message": "Search filter report fail",
        "success": False
    }


@router.post("/action", response_description="Report data action from the database", response_model=Response)
async def action_report(filter_dic: ActionReport = Body(...)):
    if filter_dic.action:
        try:
            check = CheckAction(filter_dic.action)
        except:
            return {
                "status_code": 404,
                "message": "Lỗi giá trị Action",
                "success": False
            }
    if filter_dic.action.value == 'delete':
        if filter_dic.ids:
            list_pydanticobject_ids = []
            new_data = {"active": False}
            for id_obj in filter_dic.ids:
                list_pydanticobject_ids.append(PydanticObjectId(id_obj))
            action_delete = await update_many_report(list_pydanticobject_ids, new_data)
            if action_delete:
                return {
                    "status_code": 200,
                    "detail": [],
                    "message": "Delete success",
                    "success": True
                }
            else:
                return {
                    "status_code": 404,
                    "message": "Delete fail",
                    "success": False
                }
        else:
            if filter_dic.tlp:
                for value_tlp in filter_dic.tlp:
                    try:
                        check = CheckTlpEnum(value_tlp)
                    except:
                        return {
                            "status_code": 404,
                            "message": "Lỗi giá trị TLP",
                            "success": False
                        }
            if filter_dic.status:
                for value_status in filter_dic.status:
                    try:
                        check = StatusEnum(value_status)
                    except:
                        return {
                            "status_code": 404,
                            "message": "Lỗi giá trị status",
                            "success": False
                        }
            if filter_dic.type:
                for value_type in filter_dic.type:
                    try:
                        check = CheckTypeEnum(value_type)
                    except:
                        return {
                            "status_code": 404,
                            "message": "Lỗi giá trị type",
                            "success": False
                        }
            filter_all_reports = await search_report_by_filter(filter_dic)
            if filter_all_reports:
                list_action_delete = []
                new_data = {"active": False}
                for rec in filter_all_reports:
                    list_action_delete.append(rec.id)
                action_delete = await update_many_report(list_action_delete, new_data)
                if action_delete:
                    return {
                        "status_code": 200,
                        "detail": [],
                        "message": "Delete success",
                        "success": True
                    }
            else:
                return {
                    "status_code": 404,
                    "message": "Delete fail",
                    "success": False
                }
    elif filter_dic.action.value == 'export':
        directory = f"{config.get('FOLDER_STORE_FILE')}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        if filter_dic.ids:
            list_object_ids = []
            for id_obj in filter_dic.ids:
                list_object_ids.append(PydanticObjectId(id_obj))
            data_find = {"_id": {"$in": list_object_ids}}
            list_object = await find_report(data_find)
            if list_object:
                sheet_name = str(datetime.datetime.now().year) + "_" + str(datetime.datetime.now().month) + "_" + str(
                    datetime.datetime.now().day) + "_" + str(datetime.datetime.now().hour) + "h_" + str(
                    datetime.datetime.now().minute) + "m_" + str(datetime.datetime.now().second) + "s"
                style_string = xlwt.easyxf('font: name Times New Roman', num_format_str='#,##0.00')
                wb = xlwt.Workbook()
                ws = wb.add_sheet(f'Report_{sheet_name}')
                ws.write(0, 0, 'Id', style_string)
                ws.write(0, 1, 'Create Time')
                ws.write(0, 2, 'Published Time', style_string)
                ws.write(0, 3, 'Creator', style_string)
                ws.write(0, 4, 'Type', style_string)
                ws.write(0, 5, 'Title', style_string)
                ws.write(0, 6, 'Language', style_string)
                ws.write(0, 7, 'Status', style_string)
                row = 1
                for obj in list_object:
                    ws.write(row, 0, obj.code_report, style_string)
                    ws.write(row, 1, obj.create_time.strftime("%d-%m-%Y, %H:%M:%S"), style_string)
                    if obj.published_time:
                        ws.write(row, 2, obj.published_time.strftime("%d-%m-%Y, %H:%M:%S"), style_string)
                    ws.write(row, 3, obj.creator, style_string)
                    ws.write(row, 4, obj.type, style_string)
                    ws.write(row, 5, obj.title, style_string)
                    ws.write(row, 6, obj.language, style_string)
                    ws.write(row, 7, obj.status, style_string)
                    row += 1
                wb.save(f"{config.get('FOLDER_STORE_FILE')}/Report_{sheet_name}.xls")
                headers = {'Content-Disposition': 'attachment; filename="Report_{}.xls"'.format(sheet_name)}
                return FileResponse(f"{config.get('FOLDER_STORE_FILE')}/Report_{sheet_name}.xls", headers=headers)
        else:
            if filter_dic.tlp:
                for value_tlp in filter_dic.tlp:
                    try:
                        check = CheckTlpEnum(value_tlp)
                    except:
                        return {
                            "status_code": 404,
                            "message": "Lỗi giá trị TLP",
                            "success": False
                        }
            if filter_dic.status:
                for value_status in filter_dic.status:
                    try:
                        check = StatusEnum(value_status)
                    except:
                        return {
                            "status_code": 404,
                            "message": "Lỗi giá trị status",
                            "success": False
                        }
            if filter_dic.type:
                for value_type in filter_dic.type:
                    try:
                        check = CheckTypeEnum(value_type)
                    except:
                        return {
                            "status_code": 404,
                            "message": "Lỗi giá trị type",
                            "success": False
                        }
            filter_all_reports = await search_report_by_filter(filter_dic)
            if filter_all_reports:
                sheet_name = str(datetime.datetime.now().year) + "_" + str(datetime.datetime.now().month) + "_" + str(
                    datetime.datetime.now().day) + "_" + str(datetime.datetime.now().hour) + "h_" + str(
                    datetime.datetime.now().minute) + "m_" + str(datetime.datetime.now().second) + "s"
                style_string = xlwt.easyxf('font: name Times New Roman', num_format_str='#,##0.00')
                wb = xlwt.Workbook()
                ws = wb.add_sheet(f'Report_{sheet_name}')
                ws.write(0, 0, 'Id', style_string)
                ws.write(0, 1, 'Create Time')
                ws.write(0, 2, 'Published Time', style_string)
                ws.write(0, 3, 'Creator', style_string)
                ws.write(0, 4, 'Type', style_string)
                ws.write(0, 5, 'Title', style_string)
                ws.write(0, 6, 'Language', style_string)
                ws.write(0, 7, 'Status', style_string)
                row = 1
                for obj in filter_all_reports:
                    ws.write(row, 0, obj.code_report, style_string)
                    ws.write(row, 1, obj.create_time.strftime("%d-%m-%Y, %H:%M:%S"), style_string)
                    if obj.published_time:
                        ws.write(row, 2, obj.published_time.strftime("%d-%m-%Y, %H:%M:%S"), style_string)
                    ws.write(row, 3, obj.creator, style_string)
                    ws.write(row, 4, obj.type, style_string)
                    ws.write(row, 5, obj.title, style_string)
                    ws.write(row, 6, obj.language, style_string)
                    ws.write(row, 7, obj.status, style_string)
                    row += 1
                wb.save(f"{config.get('FOLDER_STORE_FILE')}/Report_{sheet_name}.xls")
                headers = {'Content-Disposition': 'attachment; filename="Report_{}.xls"'.format(sheet_name)}
                return FileResponse(f"{config.get('FOLDER_STORE_FILE')}/Report_{sheet_name}.xls", headers=headers)


@router.post("/update", response_description="Report data action from the database", response_model=Response)
async def update_report(data_update: UpdateReport = Body(...)):
    if data_update.object_id:
        report = await get_one_report(data_update.object_id)
        if not report or not report.active:
            return {
                "status_code": 404,
                "message": "Object_id not exit!!!",
                "success": False
            }
        else:
            if data_update.tag:
                all_tag = await get_all_tag()
                if not all_tag:
                    for rec in data_update.tag:
                        tag_name = Tag(name=rec)
                        await add_tag(tag_name)
                else:
                    list_tag_name = []
                    for tag in all_tag:
                        list_tag_name.append(tag.name)
                    for rec in data_update.tag:
                        if rec not in list_tag_name:
                            tag_name = Tag(name=rec)
                            await add_tag(tag_name)
            if data_update.tlp:
                try:
                    check = CheckTlpEnum(data_update.tlp)
                except:
                    return {
                        "status_code": 404,
                        "message": "Lỗi giá trị TLP",
                        "success": False
                    }
            if data_update.type:
                for value_type in data_update.type:
                    try:
                        check = CheckTypeEnum(value_type)
                    except:
                        return {
                            "status_code": 404,
                            "message": "Lỗi giá trị type",
                            "success": False
                        }
            if report.language == data_update.language:
                new_data = {
                    "published_time": datetime.datetime.now(),
                    "type": data_update.type,
                    "title": data_update.title,
                    "tlp": data_update.tlp.value,
                    "tag": data_update.tag,
                    "description": data_update.description,
                    "detail": data_update.detail,
                    "status": 1
                }
                if data_update.group_id:
                    new_data["group_id"] = data_update.group_id
                report_update = await update_one_report(report.id, new_data)
                if report_update:
                    report_updated = await get_one_report(report.id)
                    history = History(
                        parent_id=str(report_updated.id),
                        time_action=datetime.datetime.now(),
                        action_name="edit",
                        actor=report_updated.creator
                    )
                    create_history = await add_history(history)
                    if create_history:
                        return {
                            "status_code": 200,
                            "detail": report_updated,
                            "message": "Update success!!!",
                            "success": True
                        }
                    else:
                        return {
                            "status_code": 404,
                            "detail": [],
                            "message": "Create history fail!!!",
                            "success": False
                        }
                else:
                    return {
                        "status_code": 404,
                        "detail": [],
                        "message": "Update fail!!!",
                        "success": False
                    }
            else:
                new_data = {
                    "published_time": datetime.datetime.now(),
                    "type": data_update.type,
                    "tlp": data_update.tlp.value,
                    "tag": data_update.tag,
                    "status": 1
                }
                if data_update.group_id:
                    new_data["group_id"] = data_update.group_id
                report_update = await update_one_report(report.id, new_data)
                report_updated = await get_one_report(report.id)
                if report_update:
                    history = History(
                        parent_id=str(report_updated.id),
                        time_action=datetime.datetime.now(),
                        action_name="edit",
                        actor=report_updated.creator
                    )
                    create_history = await add_history(history)
                    if create_history:
                        query = {"languages_parent_id": str(report_updated.id), "language": data_update.language}
                        find_other_language_ti_report = await find_report(query)
                        if find_other_language_ti_report:
                            new_data = {
                                "type": data_update.type,
                                "tlp": data_update.tlp.value,
                                "tag": data_update.tag,
                                "title": data_update.title,
                                "description": data_update.description,
                                "detail": data_update.detail,
                                "status": 1
                            }
                            ti_report_other_language_update = await update_one_report(
                                find_other_language_ti_report[0].id,
                                new_data
                            )
                            if ti_report_other_language_update:
                                ti_report_other_language_updated = await get_one_report(
                                    find_other_language_ti_report[0].id)
                                if ti_report_other_language_updated:
                                    del ti_report_other_language_updated.id
                                    del ti_report_other_language_updated.code_report
                                    del ti_report_other_language_updated.published_time
                                    del ti_report_other_language_updated.languages_parent_id
                                return {
                                    "status_code": 200,
                                    "detail": {
                                        "VI": report_updated,
                                        "{}".format(data_update.language): ti_report_other_language_updated
                                    },
                                    "message": "Update success!!!",
                                    "success": True
                                }
                            else:
                                return {
                                    "status_code": 404,
                                    "detail": [],
                                    "message": "Update fail!!!",
                                    "success": False
                                }
                        else:
                            child_report = TiReport(
                                type=data_update.type,
                                title=data_update.title,
                                tlp=data_update.tlp,
                                tag=data_update.tag,
                                description=data_update.description,
                                detail=data_update.detail,
                                create_time=datetime.datetime.now(),
                                creator=report_updated.creator,
                                language=data_update.language,
                                languages_parent_id=str(report_updated.id),
                                status=report_updated.status,
                                mark=report_updated.mark,
                                active=report_updated.mark,
                                group_id=report_updated.group_id
                            )
                            new_language_report = await insert_ti_report(child_report)
                            if new_language_report:
                                return {
                                    "status_code": 200,
                                    "detail": {
                                        "VI": report_updated,
                                        "{}".format(data_update.language): new_language_report
                                    },
                                    "message": "Update success!!!",
                                    "success": True
                                }
                            else:
                                return {
                                    "status_code": 404,
                                    "detail": [],
                                    "message": "Create ti_report new language fail!!!",
                                    "success": False
                                }
                    else:
                        return {
                            "status_code": 404,
                            "detail": [],
                            "message": "Create history fail!!!",
                            "success": False
                        }
                else:
                    return {
                        "status_code": 404,
                        "detail": [],
                        "message": "Update fail!!!",
                        "success": False
                    }


@router.put("/{id}", response_description="report data retrieved")
async def get_report(id_obj: str):
    report = await get_one_report(id_obj)
    if report:
        attachmemt = await retrieve_attachment(str(report.id))
        history = await retrieve_history(str(report.id))
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Report data retrieved successfully",
            "data": {"report": report,
                     "attachment": attachmemt,
                     "history": history},
        }
    else:
        return {
            "status_code": 404,
            "detail": [],
            "message": "Not find report!!!",
            "success": False
        }
