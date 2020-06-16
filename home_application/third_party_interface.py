# _*_ coding: utf-8 _*_
from blueapps.utils.logger import logger


def get_cc_hosts(client, start=0, limit=20, bk_biz_id=None):
    """
    调用第三方接口，获取主机信息
    """
    kwargs = {
        "page": {
            "start": start,
            "limit": limit
        }
    }
    if bk_biz_id:
        kwargs["bk_biz_id"] = bk_biz_id

    try:
        res = client.cc.search_host(kwargs)
    except Exception as e:
        logger.error(e)
        return None

    return handle_host_infos(res["data"]["info"])


def get_cc_businesses(start, limit, client):
    """
     调用第三方接口，获取业务信息
    """
    kwargs = {
        "page": {
            "start": start,
            "limit": limit
        }
    }
    try:
        res = client.cc.search_business(kwargs)
    except Exception as e:
        logger.error(e)
        return None

    return res["data"]["info"]


def handle_host_infos(data):
    """清洗从第三方接口获取到的主机信息"""
    clean_data = []
    for item in data:
        clean_data.append({
            "bk_cloud_id": item["host"]["bk_cloud_id"][0]["id"],
            "bk_cpu": item["host"].get("bk_cpu", ""),
            "bk_os_name": item["host"].get("bk_os_name", ""),
            "bk_host_id": item["host"].get("bk_host_id", ""),
            "bk_host_innerip": item["host"].get("bk_host_innerip", ""),
            "bk_os_bit": item["host"].get("bk_os_bit", ""),
            "create_time": item["host"].get("create_time", "")
        })

    return clean_data
