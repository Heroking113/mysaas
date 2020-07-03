# -*- coding: utf-8 -*-
import datetime

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, action

from blueking.component.shortcuts import get_client_by_request

from home_application.tasks import get_cc_hosts, get_cc_businesses
from home_application.utils import save_bk_token_to_db, get_bk_token_by_request
from home_application.decorators import calculate_func_execute_time
from home_application.models import Host, Business, Mission, MissionRecord
from home_application.common import CustomResponse, CustomPagination, handle_execute_script
from home_application.serializers import (
    HostSerializer, BusinessSerializer, MissionSerializer, MissionRecordSerializer
)


# @calculate_func_execute_time
def index(request):
    """
    前后端分离模式:跳转到前端首页
    """
    bk_token = get_bk_token_by_request(request)
    get_cc_businesses.delay(bk_token)
    return render(request, "index.html")


# def deliever_log(request):
#     return JsonResponse(data={"name": "heroking"})


@api_view(['GET'])
def retrieve_host(request):
    """
    用基于函数的视图实现对主机信息的筛选

    @api {GET} /retrieve_host/ 获取筛选后的主机信息
    @apiName RetrieveHost

    @apiParam   {String}   bk_biz_id       业务ID

    @apiSuccess {String}  bk_cloud_id      云区域ID
    @apiSuccess {Integer} bk_cpu           核数
    @apiSuccess {String}  bk_os_name       操作系统名称
    @apiSuccess {Integer} bk_host_id       主机ID
    @apiSuccess {String}  bk_host_innerip  内网IP
    @apiSuccess {String}  bk_os_bit        位数
    @apiSuccess {String}  create_time      创建时间

    @apiSuccess Example {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "result": true,
        "code": 200,
        "message": "success",
        "data": [
            {
                "bk_cloud_id": "0",
                "bk_cpu": 4,
                "bk_os_name": "linux centos",
                "bk_host_id": 2,
                "bk_host_innerip": "10.0.2.11",
                "bk_os_bit": "64-bit",
                "create_time": "2019-10-11T19:08:52.647+08:00"
            },
            {
                "bk_cloud_id": "0",
                "bk_cpu": 8,
                "bk_os_name": "linux centos",
                "bk_host_id": 3,
                "bk_host_innerip": "10.0.2.2",
                "bk_os_bit": "64-bit",
                "create_time": "2019-10-11T19:08:57.355+08:00"
            },
            {
                "bk_cloud_id": "0",
                "bk_cpu": 4,
                "bk_os_name": "linux centos",
                "bk_host_id": 7,
                "bk_host_innerip": "10.0.2.6",
                "bk_os_bit": "64-bit",
                "create_time": "2020-02-19T17:00:29.844+08:00"
            }
        ]
    }
    """
    bk_biz_id = request.query_params.get("bk_biz_id", "")
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    host_id = Host.objects.create(create_time=create_time)
    # 调用周期任务
    get_cc_hosts.delay(request=request, bk_biz_id=bk_biz_id)

    # client = get_client_by_request(request)
    # data = get_cc_hosts(client, bk_biz_id=bk_biz_id)
    host_querysets = Host.objects.all()
    host_serializer = HostSerializer(host_querysets, many=True)
    return CustomResponse(data=host_serializer.data)


@api_view(['GET'])
def query_host_by_business(request):
    querysets = Host.objects.filter(bk_biz_id=request.query_params["bk_biz_id"])
    serializer = HostSerializer(querysets, many=True)
    return CustomResponse(data=serializer.data)


@api_view(['GET'])
def query_all_info(request):
    """
    在页面初始化的时候，在该接口返回 主机信息、业务信息以及任务信息
    (如果数据量很大的时候，可以减少带宽压力)

    @api {GET} /query_all_info/ 获取所有的信息
    @apiName queryAllInfo

    @apiSuccess {Array} host_data      主机信息
    @apiSuccess {Array} business_data  业务信息
    @apiSuccess {Array} mission_data    任务信息

    @apiSuccess Example {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "result": true,
        "code": 200,
        "message": "success",
        "data": {
            "host_data": [
                {
                    "bk_cloud_id": "0",
                    "bk_cpu": 4,
                    "bk_os_name": "linux centos",
                    "bk_host_id": "2",
                    "bk_host_innerip": "10.0.2.11",
                    "bk_os_bit": "64-bit",
                    "create_time": "2019-10-11T19:08:52.647000+08:00"
                },
                {
                    "bk_cloud_id": "0",
                    "bk_cpu": 8,
                    "bk_os_name": "linux centos",
                    "bk_host_id": "3",
                    "bk_host_innerip": "10.0.2.2",
                    "bk_os_bit": "64-bit",
                    "create_time": "2019-10-11T19:08:57.355000+08:00"
                },
                {
                    "bk_cloud_id": "0",
                    "bk_cpu": 8,
                    "bk_os_name": "linux centos",
                    "bk_host_id": "4",
                    "bk_host_innerip": "10.0.2.15",
                    "bk_os_bit": "64-bit",
                    "create_time": "2019-10-11T19:09:03.441000+08:00"
                },
                {
                    "bk_cloud_id": "0",
                    "bk_cpu": 8,
                    "bk_os_name": "linux centos",
                    "bk_host_id": "5",
                    "bk_host_innerip": "10.0.2.8",
                    "bk_os_bit": "64-bit",
                    "create_time": "2019-10-11T19:09:07.770000+08:00"
                },
                {
                    "bk_cloud_id": "0",
                    "bk_cpu": null,
                    "bk_os_name": "",
                    "bk_host_id": "6",
                    "bk_host_innerip": "10.0.1.103",
                    "bk_os_bit": "",
                    "create_time": "2020-02-19T15:36:56.852000+08:00"
                },
                {
                    "bk_cloud_id": "0",
                    "bk_cpu": 4,
                    "bk_os_name": "linux centos",
                    "bk_host_id": "7",
                    "bk_host_innerip": "10.0.2.6",
                    "bk_os_bit": "64-bit",
                    "create_time": "2020-02-19T17:00:29.844000+08:00"
                },
                {
                    "bk_cloud_id": "0",
                    "bk_cpu": 1,
                    "bk_os_name": "linux centos",
                    "bk_host_id": "8",
                    "bk_host_innerip": "10.0.2.13",
                    "bk_os_bit": "64-bit",
                    "create_time": "2020-04-21T16:35:47.281000+08:00"
                },
                {
                    "bk_cloud_id": "0",
                    "bk_cpu": 1,
                    "bk_os_name": "linux centos",
                    "bk_host_id": "9",
                    "bk_host_innerip": "10.0.2.7",
                    "bk_os_bit": "64-bit",
                    "create_time": "2020-04-21T16:35:48.089000+08:00"
                },
                {
                    "bk_cloud_id": "0",
                    "bk_cpu": 1,
                    "bk_os_name": "linux centos",
                    "bk_host_id": "10",
                    "bk_host_innerip": "10.0.2.16",
                    "bk_os_bit": "64-bit",
                    "create_time": "2020-04-21T16:36:39.943000+08:00"
                }
            ],
            "business_data": [
                {
                    "bk_biz_id": "2",
                    "bk_biz_name": "蓝鲸"
                },
                {
                    "bk_biz_id": "3",
                    "bk_biz_name": "测试业务"
                },
                {
                    "bk_biz_id": "5",
                    "bk_biz_name": "流程管理服务"
                },
                {
                    "bk_biz_id": "6",
                    "bk_biz_name": "实验专用业务"
                }
            ],
            "mission_data": [
                {
                    "mission_name": "CPU占用最多的前10个进程",
                    "mission_content": "auxw|head -1;ps auxw|sort -rn -k3|head -10"
                },
                {
                    "mission_name": "查看各分区使用情况",
                    "mission_content": "df -h"
                }
            ]
        }
    }
    """
    # 异步任务
    bk_token = get_bk_token_by_request(request)
    get_cc_businesses.delay(bk_token)
    # 获取主机信息
    host_querysets = Host.objects.all()
    if host_querysets:
        host_serializer = HostSerializer(host_querysets, many=True)
        host_data = host_serializer.data
    else:
        host_data = ""

    # 获取业务信息
    business_querysets = Business.objects.all()
    if business_querysets:
        business_serializer = BusinessSerializer(business_querysets, many=True)
        business_data = business_serializer.data
    else:
        business_data = ""

    # 获取任务信息
    mission_querysets = Mission.objects.all()
    mission_serializer = MissionSerializer(mission_querysets, many=True)
    mission_data = mission_serializer.data

    res_data = {
        "host_data": host_data,
        "business_data": business_data,
        "mission_data": mission_data
    }

    return CustomResponse(data=res_data)


@api_view(['POST'])
def execute_script(request):
    """
    执行脚本

    @api {POST} /execute_script/ 获取所有的信息
    @apiName executeScript

    @apiParam {String} bk_biz_id     业务ID
    @apiParam {String}  bk_biz_name   业务名称
    @apiParam {String} script_content  脚本内容
    @apiParam {String}  mission_name   任务名称
    @apiParam {Array}  host_list   主机列表信息

    @apiSuccess Example {json} Success-Response:
    HTTP/1.1 200 OK
    {
        code: 200
        data: {res: "doing"}
        message: "doing"
        result: true
    }
    """
    class JobStatus(object):
        SUCCESS = "success"
        DOING = "doing"
        FAIL = "fail"

    res = handle_execute_script(request)
    if res == JobStatus.SUCCESS:
        return CustomResponse(message=JobStatus.SUCCESS)
    elif res == JobStatus.DOING:
        return CustomResponse(message=JobStatus.DOING)
    return CustomResponse(message=JobStatus.FAIL)


class MissionRecordViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MissionRecordSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return MissionRecord.query_records_with_condition(self.request).order_by("id")

    def list(self, request, *args, **kwargs):
        """
        @api {GET} /records/ 获取任务的执行记录
        @apiName queryRecord

        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "result": true,
            "code": 200,
            "messsage": "success",
            "count": 17,
            "data": [
                {
                    "id": 1,
                    "status": "执行成功",
                    "business_name": "测试业务",
                    "mission_name": "查看当前工作目录路径",
                    "machine_num": 2,
                    "operator": "1819785416",
                    "create_time": "2020-06-12T13:02:24.583226+08:00"
                },
                {
                    "id": 2,
                    "status": "执行成功",
                    "business_name": "测试业务",
                    "mission_name": "查看当前工作目录路径",
                    "machine_num": 2,
                    "operator": "1819785416",
                    "create_time": "2020-06-12T13:04:25.001168+08:00"
                },
                {
                    "id": 3,
                    "status": "执行成功",
                    "business_name": "测试业务",
                    "mission_name": "查看当前工作目录路径",
                    "machine_num": 2,
                    "operator": "1819785416",
                    "create_time": "2020-06-12T13:04:52.013939+08:00"
                }
            ]
        }
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(data=serializer.data)

    @action(["GET"], detail=False)
    def conditions(self, request, *args, **kwargs):
        """
         @api {GET} /records/conditions/ 获取任务记录的筛选条件
         @apiName queryRecordsConditions

         @apiSuccess Example {json} Success-Response:
         HTTP/1.1 200 OK
         {
            "result": true,
            "code": 200,
            "message": "success",
            "data": {
                "operators": [
                    "1819785416"
                ],
                "businesses": [
                    "蓝鲸",
                    "测试业务"
                ],
                "missions": [
                    "占用内存最高的前10个进程",
                    "查看当前工作目录路径"
                ]
            }
         }
        """
        queryset = self.filter_queryset(self.get_queryset())

        operators = []
        businesses = []
        missions = []
        for item in queryset.values():
            operators.append(item.get("operator"))
            businesses.append(item.get("business_name"))
            missions.append(item.get("mission_name"))

        ret_data = {
            "operators": list(set(operators)),
            "businesses": list(set(businesses)),
            "missions": list(set(missions))
        }
        return CustomResponse(data=ret_data)
