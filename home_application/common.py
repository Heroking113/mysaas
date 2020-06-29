# _*_ coding: utf-8 _*_
import json
from collections import OrderedDict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from blueking.component.shortcuts import get_client_by_request

from home_application.models import MissionRecord
from home_application.tasks import async_handle_execute_script


class CustomResponse(Response):
    class RetConstant(object):
        CODE_SUCCESS = 200
        MSG_SUCCESS = "success"

    def __init__(self,
                 code=RetConstant.CODE_SUCCESS,
                 message=RetConstant.MSG_SUCCESS,
                 data=None,
                 result=True,
                 status_=status.HTTP_200_OK,
                 content_type='application/json'
                 ):
        super(Response, self).__init__(None, status=status_)
        self._code = code
        self._message = message
        self._data = data
        self._result = result
        self.content_type = content_type

        self.data = {"result": result, "code": code, "message": message, "data": data}

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def result(self):
        return self._result

    @message.setter
    def result(self, value):
        self._result = value


class CustomPagination(PageNumberPagination):
    page_size = 8
    max_page_size = 50
    page_query_param = "page"
    page_size_query_param = page_size

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ("result", True),
            ("code", 200),
            ("messsage", "success"),
            ('count', self.page.paginator.count),
            ("data", data)
        ]))


def handle_execute_script(request):
    """
    将任务信息记录到数据库，并通过异步任务执行脚本，将执行状态更新到数据库
    """
    client = get_client_by_request(request)
    bk_biz_id = request.data.get("bk_biz_id", "")
    host_list = json.loads(request.data.get("host_list"))
    user = request.user.username
    business_name = request.data.get("business_name", "")
    mission_name = request.data.get("mission_name", "")

    ip_list = [{"bk_cloud_id": int(item["bk_cloud_id"]), "ip": item["bk_host_innerip"]} for item in host_list]
    kwargs = {
        "bk_biz_id": int(bk_biz_id),
        "ip_list": ip_list,
        "script_id": 116,
        "user": user,
        "account": "root"
    }
    # 把数据存入数据库
    queryset = MissionRecord.objects.create(
        business_name=business_name,
        mission_name=mission_name,
        machine_num=len(host_list),
        operator=user
    )
    # 执行异步任务
    async_result = async_handle_execute_script.delay(kwargs, record_id=queryset.id)
    if async_result.ready():
        res = async_result.get()
    else:
        res = "doing"

    return res
