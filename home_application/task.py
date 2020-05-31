# _*_ coding: utf-8 _*_

from __future__ import absolute_import, unicode_literals

import datetime

from django.http import JsonResponse

from blueapps.utils.logger import logger
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from home_application.models import ScriptSearch, FastExecuteScript


@task
def execute_script(request, client):
    # 根据前端的business_name获取对应的bk_biz_id
    business_data = client.cc.search_business()["data"]["info"]
    bk_biz_id = ''
    for business_item in business_data:
        if business_item["bk_biz_name"] == request.GET.get("business_name", ""):
            bk_biz_id = business_item["bk_biz_id"]
            break

    # 根据前端传来的host_ips获取bk_cloud_id
    # host_data = client.cc.search_host()
    host_data = client.cc.search_host({"bk_biz_id": bk_biz_id})["data"]["info"]
    bk_cloud_id = []
    host_ips = request.GET.get("host_ips", "")
    for host_item in host_data:
        if host_item["host"]["bk_host_innerip"] in host_ips:
            bk_cloud_id.append(host_item["host"]["bk_cloud_id"][0]["id"])
            break

    bk_cloud_id = ",".join(bk_cloud_id)
    # 把要执行的相关信息存入数据表
    fastexecutescript = FastExecuteScript(bk_biz_id=bk_biz_id, bk_cloud_id=bk_cloud_id, bk_host_ip=host_ips)
    fastexecutescript.save()

    bk_cloud_id = bk_cloud_id.split(",")
    ip = host_ips.split(",")
    ip_list = []
    for index in range(len(bk_cloud_id)):
        ip_list.append({
            "bk_cloud_id": bk_cloud_id[index],
            "ip": ip[index]
        })

    # 获取查询脚本
    to_execute_script = ScriptSearch.objects.get(name=request.GET.get("script_name"))
    script_content = to_execute_script.content
    # 拼接参数
    fast_kwargs = {
        "account": "root",
        "bk_biz_id": bk_biz_id,
        "script_content": script_content,
        "ip_list": ip_list
    }
    fast_result = client.job.fast_execute_script(fast_kwargs)

    if fast_result["result"]:
        job_instance_status_kwargs = {
            "bk_biz_id": bk_biz_id,
            "job_instance_id": fast_result["data"]["job_instance_id"]
        }
        JOB_DOING = 2
        while(True):
            job_instance_status_result = client.job.get_job_instance_status(job_instance_status_kwargs)
            if job_instance_status_result["result"]:
                if job_instance_status_result["data"]["job_instance"]["status"] == JOB_DOING:
                    continue
                return JsonResponse(job_instance_status_result)
            else:
                return JsonResponse(job_instance_status_result)
    return JsonResponse(fast_result)