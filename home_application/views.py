# -*- coding: utf-8 -*-
import json

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blueapps.patch.settings_open_saas import SITE_URL
from blueking.component.shortcuts import get_client_by_request

from home_application.models import ScriptSearch, FastExecuteScript
from home_application.serializers import ScriptSearchSerializer
from home_application.task import execute_script


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt


def index(request):
    """
    首页:永久跳转到‘执行任务’界面
    """
    # return HttpResponsePermanentRedirect('/execute-mission/')
    return HttpResponsePermanentRedirect(SITE_URL + '/execute-mission/')


def execute_mission(request):
    # 调用开发的云API接口
    client = get_client_by_request(request)
    business_data = client.cc.search_business()["data"]["info"]
    business_data.append({"bk_biz_name": ""})
    business_data.reverse()
    host_data = client.cc.search_host()
    script_contents = ScriptSearch.objects.all()
    serializer = ScriptSearchSerializer(script_contents, many=True)
    script_data = serializer.data
    return render(request,
                  'home_application/execute_mission.html',
                  {
                      "business_data": business_data,
                      "script_data": script_data,
                      "host_data": host_data["data"]["info"],
                      "site_url": json.dumps(SITE_URL)
                  })


def mission_record(request):
    return render(request, 'home_application/mission_record.html')


def query_host_info(request):
    # 调用开发的云API接口
    client = get_client_by_request(request)

    business_data = client.cc.search_business()
    business_data = business_data["data"]["info"]

    bk_biz_id = None
    for business_item in business_data:
        if business_item["bk_biz_name"] == request.GET.get("business_name", ""):
            bk_biz_id = business_item["bk_biz_id"]
            break
    host_data = client.cc.search_host({"bk_biz_id": bk_biz_id})["data"]["info"]

    return JsonResponse({
        "result": True,
        "code": 0,
        "host_data": host_data
    })


def query_specific_host(request):
    client = get_client_by_request(request)
    # return execute_script(request, client)
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
