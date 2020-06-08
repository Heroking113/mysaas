# _*_ coding: utf-8 _*_

import time

from django.http import JsonResponse

from blueking.component.shortcuts import get_client_by_request

from home_application.models import FastExecuteScript, ScriptJobRecord, HostInfo, BusinessInfo
from home_application.task import async_handle_execute_script


def pkg_execute_script_kwargs(kwargs, client):
    bk_biz_id = kwargs.get("bk_biz_id", "")

    # 根据前端传来的host_ips获取bk_cloud_id
    host_data = client.cc.search_host({"bk_biz_id": bk_biz_id})["data"]["info"]
    bk_cloud_id = ''
    host_ips = kwargs.get("host_ips", [])
    for host_item in host_data:
        if host_item["host"]["bk_host_innerip"] in host_ips:
            bk_cloud_id = host_item["host"]["bk_cloud_id"][0]["id"]
            break

    # 把要执行的相关信息存入数据表
    fastexecutescript = FastExecuteScript.objects.create(
        bk_biz_id=bk_biz_id,
        bk_cloud_id=bk_cloud_id,
        bk_host_ip=host_ips
    )
    host_ips = host_ips.split(",")
    ip_list = [{"bk_cloud_id": bk_cloud_id, "ip": host_ips[i]} for i in range(len(bk_cloud_id))]

    # 获取查询脚本
    business_data = client.cc.search_business()["data"]["info"]

    bk_biz_name = None
    for business_item in business_data:
        if business_item["bk_biz_id"] == int(kwargs["bk_biz_id"]):
            bk_biz_name = business_item["bk_biz_name"]
            break
    script_job_record = ScriptJobRecord.objects.create(
        business=bk_biz_name,
        mission=kwargs["script"],
        operator=kwargs["user"],
        machine_num=len(host_ips)
    )
    record_id = script_job_record.id
    # 拼接参数
    fast_kwargs = {
        "account": "root",
        "bk_biz_id": bk_biz_id,
        "script_id": 116,
        "ip_list": ip_list,
        "record_id": record_id
    }

    return fast_kwargs


def pkg_query_records():
    queryset = ScriptJobRecord.objects.all()
    users = []
    businesses = []
    missions = []
    records = []
    for item in queryset:
        dic_data = {
            "operator": item.operator,
            "business": item.business,
            "mission": item.mission,
            "start_time": item.start_time,
            "machine_num": item.machine_num,
            "status": item.status
        }
        records.append(dic_data)

    for item in records:
        users.append(item.get("operator"))
        businesses.append(item.get("business"))
        missions.append(item.get("mission"))
    users = list(set(users))
    users.append("所有用户")
    users.reverse()
    businesses = list(set(businesses))
    businesses.append("所有业务")
    businesses.reverse()
    missions = list(set(missions))
    missions.append("所有任务")
    missions.reverse()

    return {
            "users": users,
            "businesses": businesses,
            "missions": missions,
            "all_info": records
        }


def pkg_retrieve_kwargs(request):
    business = "" if request.GET.get("business") == "所有业务" else request.query_params.get("business", "")
    operator = "" if request.GET.get("operator") == "所有用户" else request.query_params.get("operator", "")
    mission = "" if request.GET.get("mission") == "所有任务" else request.query_params.get("mission", "")
    kwargs = {}
    if business:
        kwargs["business"] = business
    if operator:
        kwargs["operator"] = operator
    if mission:
        kwargs["mission"] = mission

    return kwargs


def get_host_data(client):
    """
    获取主机信息
    """
    host_querysets = HostInfo.objects.all()
    if not host_querysets.exists():
        # 如果数据库中没有数据，则调用 search_host 接口，获取主机信息，并将其存入数据库
        res_data = client.cc.search_host()["data"]["info"]
        host_data = []
        for item in res_data:
            bk_host_innerip = item["host"].get("bk_host_innerip", "")
            bk_os_name = item["host"].get("bk_os_name", "")
            host_data.append(HostInfo(bk_host_innerip=bk_host_innerip, bk_os_name=bk_os_name))
        host_querysets = HostInfo.objects.bulk_create(host_data)

    return host_querysets


def get_business_data(client):
    """
     获取业务信息
    """
    business_querysets = BusinessInfo.objects.all()
    if not business_querysets.exists():
        # 如果数据库中没有数据，则调用 search_business 接口，获取业务信息，并将其存入数据库
        res_data = client.cc.search_business()["data"]["info"]
        business_data = []
        for item in res_data:
            bk_biz_id = item.get("bk_biz_id", "")
            bk_biz_name = item.get("bk_biz_name", "")
            business_data.append(BusinessInfo(bk_biz_id=bk_biz_id, bk_biz_name=bk_biz_name))
        business_querysets = BusinessInfo.objects.bulk_create(business_data)

    return business_querysets


def handle_execute_script(request):
    client = get_client_by_request(request)
    req_kwargs = {}
    req_kwargs["bk_biz_id"] = request.POST.get("bk_biz_id", "")
    req_kwargs["script"] = request.POST.get("script", "")
    req_kwargs["host_ips"] = request.POST.get("host_ips", "")
    req_kwargs["user"] = request.user.username
    # 封装参数
    kwargs = pkg_execute_script_kwargs(req_kwargs, client)
    # 异步执行
    async_handle_execute_script.delay(client, kwargs)

    # 轮询(最多轮询3次)
    SEARCH_COUNT = 0
    while True:
        script_job_record = ScriptJobRecord.objects.get(pk=kwargs["record_id"])
        status = script_job_record.status
        if status is not None or SEARCH_COUNT > 2:
            is_true = status == str(True)
            condition = True if is_true else False
            return JsonResponse({
                "message": "success",
                "condition": condition,
                "data": {}
            })
        SEARCH_COUNT += 1
        time.sleep(1)
