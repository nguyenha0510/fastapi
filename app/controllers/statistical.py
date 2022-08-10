from fastapi import APIRouter, Body

from app.services.statistical_service import *
from app.services.ti_report_service import *
from models.statistical import *

router = APIRouter()


@router.post("/get_statistical", response_description="Get Statistical data from database", response_model=Response)
async def get_statistical(filter_dic: FilterStatistical = Body(...)):
    filter_dic = dict(filter_dic)
    statiscal = await statistical_data(filter_dic)
    if statiscal:
        return {
            "status_code": 200,
            "detail": statiscal,
            "message": "Search all success",
            "success": True
        }
    return {
        "status_code": 404,
        "message": "Search all report fail",
        "success": False
    }


@router.get("/get_config", response_description="Get config to statistical data ", response_model=Response)
async def get_config():
    count_creator = await aggregate_report()
    data_config = {
        "tlp": {
            "red": "Red",
            "amber": "Amber",
            "green": "Green",
            "white": "White",
        },
        "status": {
            1: "New",
            2: "Approve",
            5: "Reject",
        },
        "language": {
            "VI": "VI",
            "EN": "EN",
        },
        "type": {
            "attack_pattern": "Attack-pattern",
            "campaign": "Campaign",
            "identity": "Identity",
            "indicator": "Indicator",
            "intrusion_set": "Intrusion-set",
            "malware": "Malware",
            "observed_data": "Observed-data",
            "threat_actor": "Threat-actor",
            "threat_report": "Threat-report",
            "tool": "Tool",
            "vulnerability": "Vulnerability",
        },
        "creator": count_creator,
    }
    return {
        "status_code": 200,
        "detail": data_config,
        "message": "Get config success",
        "success": True
    }
