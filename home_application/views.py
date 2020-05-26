# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from blueking.component.shortcuts import get_client_by_request

from home_application.models import ScriptSearch
from home_application.serializers import ScriptSearchSerializer


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页:永久跳转到‘执行任务’界面
    """
    return HttpResponsePermanentRedirect('/execute_mission/')
    # return render(request, 'home_application/index_home.html')


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


@api_view(["POST"])
def execute_mission(request):
    # 调用开发的云API接口
    # client = get_client_by_request(request)
    # data = client.cc.search_business()
    # data = fask_execute_script(client)
    script_contents = ScriptSearch.objects.all()
    serializer = ScriptSearchSerializer(script_contents, many=True)
    data = serializer.data
    return Response(data)


@api_view(['POST'])
def mission_record(request):
    response = {
        'code': 200,
        'data': {
            'first_name': 'hero',
            'last_name': 'king'
        }
    }
    return JsonResponse(response)
    # return Response(data)
    # return render(request, 'home_application/mission_record.html')

# GET in
# wrapper(in) -response
    # call data = mission_record
    # response = normalized data
# wrapper(out)
# GET(out)
