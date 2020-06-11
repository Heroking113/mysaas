# _*_ coding: utf-8 _*_

from __future__ import absolute_import, unicode_literals

import datetime

from blueking.component.shortcuts import get_client_by_request
from blueapps.utils.logger import logger
from celery import task
# from home_application.models import ScriptJobRecord
from celery.schedules import crontab
from celery.task import periodic_task

# from home_application.models import ScriptSearch, FastExecuteScript


@task()
def async_handle_execute_script(client, kwargs):
    result = client.job.fast_execute_script(kwargs)
    # script_job_record = ScriptJobRecord.objects.filter(pk=kwargs["record_id"])
    # script_job_record.update(status=result["result"])


# 这部分拆掉，然后把需要的内容放到task中
def handle_execute_script(request):
    client = get_client_by_request(request)
    kwargs = {}
    kwargs["bk_biz_id"] = request.POST.get("bk_biz_id", "")
    kwargs["script"] = request.POST.get("script", "")
    kwargs["host_ips"] = request.POST.get("host_ips", "")
    kwargs["user"] = request.user.username
    # 异步执行
    async_handle_execute_script.delay(client, kwargs)

    # # 轮询(这一块开一个新的接口用于前端轮询)
    # SEARCH_COUNT = 0
    # while True:
    #     script_job_record = ScriptJobRecord.objects.get(pk=kwargs["record_id"])
    #     status = script_job_record.status
    #     if status is not None or SEARCH_COUNT > 2:
    #         is_true = status == str(True)
    #         condition = True if is_true else False
    #         return JsonResponse({
    #             "message": "success",
    #             "condition": condition,
    #             "data": {}
    #         })
    #     SEARCH_COUNT += 1
    #     time.sleep(1)



# 这部分放到task中
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
