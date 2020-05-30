# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blueapps.patch.settings_open_saas import SITE_URL
from blueking.component.shortcuts import get_client_by_request

from home_application.models import ScriptSearch
from home_application.serializers import ScriptSearchSerializer


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt


def index(request):
    """
    首页:永久跳转到‘执行任务’界面
    """
    return HttpResponsePermanentRedirect(SITE_URL+'/execute-mission/')


def dev_guide(request):
    """
    开发指引
    """
    return render(request, 'home_application/dev_guide.html')


def contact(request):
    """
    联系页
    """
    return render(request, 'home_application/contact.html')


def helloworld(request):
    """
    helloworld
    """
    return HttpResponse('Helloworld')


def execute_mission(request):

    # 调用开发的云API接口
    client = get_client_by_request(request)
    business_data = client.cc.search_business()
    host_data = client.cc.search_host()
    script_contents = ScriptSearch.objects.all()
    serializer = ScriptSearchSerializer(script_contents, many=True)
    script_data = serializer.data
    return render(request,
                  'home_application/execute_mission.html',
                  {
                      "business_data": business_data["data"]["info"],
                      "script_data": script_data,
                      "host_data": host_data["data"]["info"]
                  })


def mission_record(request):
    return render(request, 'home_application/mission_record.html')


def get_host_info(request):
    # 调用开发的云API接口
    client = get_client_by_request(request)

    business_data = client.cc.search_business()
    business_data = business_data["data"]["info"]

    bk_biz_id = None
    for business_item in business_data:
        if business_item["bk_biz_name"] == request.GET.get("business_name", ""):
            bk_biz_id = business_item["bk_biz_id"]
            break
    host_data = client.cc.search_host({"bk_biz_id": bk_biz_id})
    host_data = host_data["data"]["info"]

    return JsonResponse({
        "result": True,
        "code": 0,
        "host_data": host_data
    })
