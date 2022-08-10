from models.ti_report import TiReport

ti_report_collection = TiReport


async def statistical_data(filter_dict: dict) -> dict:
    query_tlp_red = {"tlp": "red", "active": True}
    query_tlp_amber = {"tlp": "amber", "active": True}
    query_tlp_green = {"tlp": "green", "active": True}
    query_tlp_white = {"tlp": "white", "active": True}
    query_status_new = {"status": 1, "active": True}
    query_status_approve = {"status": 2, "active": True}
    query_status_reject = {"status": 5, "active": True}
    query_language_vi = {"language": "VI", "active": True}
    query_language_en = {"language": "EN", "active": True}
    query_type_attack_pattern = {"type": "Attack-pattern", "active": True}
    query_type_campaign = {"type": "Campaign", "active": True}
    query_type_identity = {"type": "Identity", "active": True}
    query_type_indicator = {"type": "Indicator", "active": True}
    query_type_intrusion_set = {"type": "Intrusion-set", "active": True}
    query_type_malware = {"type": "Malware", "active": True}
    query_type_observed_data = {"type": "Observed-data", "active": True}
    query_type_threat_actor = {"type": "Threat-actor", "active": True}
    query_type_threat_report = {"type": "Threat-report", "active": True}
    query_type_tool = {"type": "Tool", "active": True}
    query_type_vulnerability = {"type": "Vulnerability", "active": True}
    if filter_dict["creator"] is not None:
        query_tlp_red["creator"] = filter_dict["creator"]
        query_tlp_amber["creator"] = filter_dict["creator"]
        query_tlp_green["creator"] = filter_dict["creator"]
        query_tlp_white["creator"] = filter_dict["creator"]
        query_status_new["creator"] = filter_dict["creator"]
        query_status_approve["creator"] = filter_dict["creator"]
        query_status_reject["creator"] = filter_dict["creator"]
        query_language_vi["creator"] = filter_dict["creator"]
        query_language_en["creator"] = filter_dict["creator"]
        query_type_attack_pattern["creator"] = filter_dict["creator"]
        query_type_campaign["creator"] = filter_dict["creator"]
        query_type_identity["creator"] = filter_dict["creator"]
        query_type_indicator["creator"] = filter_dict["creator"]
        query_type_intrusion_set["creator"] = filter_dict["creator"]
        query_type_malware["creator"] = filter_dict["creator"]
        query_type_observed_data["creator"] = filter_dict["creator"]
        query_type_threat_actor["creator"] = filter_dict["creator"]
        query_type_threat_report["creator"] = filter_dict["creator"]
        query_type_tool["creator"] = filter_dict["creator"]
        query_type_vulnerability["creator"] = filter_dict["creator"]
    if filter_dict["tag"] is not None:
        query_tlp_red["tag"] = {"$all": filter_dict["tag"]}
        query_tlp_amber["tag"] = {"$all": filter_dict["tag"]}
        query_tlp_green["tag"] = {"$all": filter_dict["tag"]}
        query_tlp_white["tag"] = {"$all": filter_dict["tag"]}
        query_status_new["tag"] = {"$all": filter_dict["tag"]}
        query_status_approve["tag"] = {"$all": filter_dict["tag"]}
        query_status_reject["tag"] = {"$all": filter_dict["tag"]}
        query_language_vi["tag"] = {"$all": filter_dict["tag"]}
        query_language_en["tag"] = {"$all": filter_dict["tag"]}
        query_type_attack_pattern["tag"] = {"$all": filter_dict["tag"]}
        query_type_campaign["tag"] = {"$all": filter_dict["tag"]}
        query_type_identity["tag"] = {"$all": filter_dict["tag"]}
        query_type_indicator["tag"] = {"$all": filter_dict["tag"]}
        query_type_intrusion_set["tag"] = {"$all": filter_dict["tag"]}
        query_type_malware["tag"] = {"$all": filter_dict["tag"]}
        query_type_observed_data["tag"] = {"$all": filter_dict["tag"]}
        query_type_threat_actor["tag"] = {"$all": filter_dict["tag"]}
        query_type_threat_report["tag"] = {"$all": filter_dict["tag"]}
        query_type_tool["tag"] = {"$all": filter_dict["tag"]}
        query_type_vulnerability["tag"] = {"$all": filter_dict["tag"]}
    count_tlp_red = await ti_report_collection.find(query_tlp_red).count()
    count_tlp_amber = await ti_report_collection.find(query_tlp_amber).count()
    count_tlp_green = await ti_report_collection.find(query_tlp_green).count()
    count_tlp_white = await ti_report_collection.find(query_tlp_white).count()
    count_status_new = await ti_report_collection.find(query_status_new).count()
    count_status_approve = await ti_report_collection.find(query_status_approve).count()
    count_status_reject = await ti_report_collection.find(query_status_reject).count()
    count_language_vi = await ti_report_collection.find(query_language_vi).count()
    count_language_en = await ti_report_collection.find(query_language_en).count()
    count_type_attack_pattern = await ti_report_collection.find(query_type_attack_pattern).count()
    count_type_campaign = await ti_report_collection.find(query_type_campaign).count()
    count_type_identity = await ti_report_collection.find(query_type_identity).count()
    count_type_indicator = await ti_report_collection.find(query_type_indicator).count()
    count_type_intrusion_set = await ti_report_collection.find(query_type_intrusion_set).count()
    count_type_malware = await ti_report_collection.find(query_type_malware).count()
    count_type_observed_data = await ti_report_collection.find(query_type_observed_data).count()
    count_type_threat_actor = await ti_report_collection.find(query_type_threat_actor).count()
    count_type_threat_report = await ti_report_collection.find(query_type_threat_report).count()
    count_type_tool = await ti_report_collection.find(query_type_tool).count()
    count_type_vulnerability = await ti_report_collection.find(query_type_vulnerability).count()
    return {
        "tlp": [
            {"value": "red", "count": count_tlp_red},
            {"value": "amber", "count": count_tlp_amber},
            {"value": "green", "count": count_tlp_green},
            {"value": "white", "count": count_tlp_white},
        ],
        "status": [
            {"value": 1, "count": count_status_new},
            {"value": 2, "count": count_status_approve},
            {"value": 5, "count": count_status_reject},
        ],
        "language": [
            {"value": "VI", "count": count_language_vi},
            {"value": "EN", "count": count_language_en},
        ],
        "type": [
            {"value": "attack_pattern", "count": count_type_attack_pattern},
            {"value": "campaign", "count": count_type_campaign},
            {"value": "identity", "count": count_type_identity},
            {"value": "indicator", "count": count_type_indicator},
            {"value": "intrusion_set", "count": count_type_intrusion_set},
            {"value": "malware", "count": count_type_malware},
            {"value": "observed_data", "count": count_type_observed_data},
            {"value": "threat_actor", "count": count_type_threat_actor},
            {"value": "threat_report", "count": count_type_threat_report},
            {"value": "tool", "count": count_type_tool},
            {"value": "vulnerability", "count": count_type_vulnerability},
        ],
    }
