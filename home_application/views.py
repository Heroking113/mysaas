# -*- coding: utf-8 -*-
"""
# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
"""
import json
import time

from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blueapps.patch.settings_open_saas import SITE_URL
from blueking.component.shortcuts import get_client_by_request

from home_application.models import ScriptSearch, FastExecuteScript, ScriptJobRecord
from home_application.serializers import ScriptSearchSerializer
from home_application.task import async_handle_execute_script

from home_application.utils import pkg_execute_script_kwargs, handle_query_records


def to_index(request):
    return HttpResponsePermanentRedirect('frontend')


def index(request):
    """
    前后端分离:跳转到前端首页
    """
    return render(request, "index.html")


    # """
    # 纯 Django 首页:永久跳转到‘执行任务’界面
    # """
    # return HttpResponsePermanentRedirect('/execute-mission/')
    # return HttpResponsePermanentRedirect(SITE_URL + 'execute-mission/')


def get_user_info(request):
    client = get_client_by_request(request)
    user = client.bk_login.get_user(bk_app_code='herokingfsaas',
                                    bk_app_secret='d9664192-989a-424e-b0e6-5acb404fee2d')
    return JsonResponse(user)

def execute_mission(request):
    # 调用开发的云API接口
    client = get_client_by_request(request)
    business_data = client.cc.search_business()["data"]["info"]
    business_data.append({"bk_biz_name": "所有业务"})
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
    context = handle_query_records()
    context["site_url"] = json.dumps(SITE_URL)
    return render(request, 'home_application/mission_record.html', {"context": context})


@csrf_exempt
def query_host_info(request):
    # 调用开发的云API接口
    client = get_client_by_request(request)

    business_data = client.cc.search_business()
    business_data = business_data["data"]["info"]

    bk_biz_id = None
    for business_item in business_data:
        if business_item["bk_biz_name"] == request.POST.get("business_name", ""):
            bk_biz_id = business_item["bk_biz_id"]
            break
    host_data = client.cc.search_host({"bk_biz_id": bk_biz_id})["data"]["info"]

    return JsonResponse({
        "result": True,
        "code": 0,
        "host_data": host_data
    })


@csrf_exempt
def execute_script(request):
    client = get_client_by_request(request)
    # 封装参数
    kwargs = pkg_execute_script_kwargs(request, client)
    # 异步执行
    async_handle_execute_script.delay(client, kwargs)

    # 轮询(最多轮询3次)
    SEARCH_COUNT = 0
    while True:
        script_job_record = ScriptJobRecord.objects.get(pk=kwargs["record_id"])
        status = script_job_record.status
        #
        if status is not None or SEARCH_COUNT > 2:
            status = status == str(True)
            res = {
                "result": status,
                "code": 0 if status else 1,
                "message": "success" if status else "fail",
                "data": {}
            }
            return JsonResponse(res)
        SEARCH_COUNT += 1
        time.sleep(1)


def query_record(request):
    business = "" if request.GET.get("business") == "所有业务" else request.GET.get("business", "")
    operator = "" if request.GET.get("operator") == "所有用户" else request.GET.get("operator", "")
    mission = "" if request.GET.get("mission") == "所有任务" else request.GET.get("mission", "")
    kwargs = {}
    if business:
        kwargs["business"] = business
    if operator:
        kwargs["operator"] = operator
    if mission:
        kwargs["mission"] = mission
    querysets = ScriptJobRecord.objects.filter(**kwargs)

    context = []
    for item in querysets:
        dic_data = {
            "operator": item.operator,
            "business": item.business,
            "mission": item.mission,
            "start_time": item.start_time,
            "machine_num": item.machine_num,
            "status": item.status
        }
        context.append(dic_data)

    return JsonResponse({
        "result": True,
        "code": 0,
        "message": "success",
        "data": context
    })
