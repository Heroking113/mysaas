# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, action

from blueking.component.shortcuts import get_client_by_request

from home_application.models import ScriptSearch, ScriptJobRecord
from home_application.utils import pkg_retrieve_kwargs, get_host_data, get_business_data, handle_execute_script
from home_application.serializers import (ScriptSearchSerializer, ScriptJobRecordSerializer,
                                          HostInfoSerializer, BusinessInfoSerializer)


def index(request):
    """
    前后端分离模式:跳转到前端首页
    """
    return render(request, "index.html")


@api_view(['GET'])
def query_all_info(request):
    """
    @api {GET} /query_all_info/ 获取所有的信息
    @apiName queryAllInfo

    @apiSuccess {Array} host_data      主机信息
    @apiSuccess {Array} business_data  业务信息
    @apiSuccess {Array} script_data    脚本信息

    @apiSuccess Example {json} Success-Response:
    HTTP/1.1 200 OK
    {
    "host_data": [
        {
            "bk_host_innerip": "10.0.2.11",
            "bk_os_name": "linux centos"
        },
        {
            "bk_host_innerip": "10.0.2.2",
            "bk_os_name": "linux centos"
        },
        {
            "bk_host_innerip": "10.0.2.15",
            "bk_os_name": "linux centos"
        },
        {
            "bk_host_innerip": "10.0.2.8",
            "bk_os_name": "linux centos"
        },
        {
            "bk_host_innerip": "10.0.1.103",
            "bk_os_name": ""
        },
        {
            "bk_host_innerip": "10.0.2.6",
            "bk_os_name": "linux centos"
        },
        {
            "bk_host_innerip": "10.0.2.13",
            "bk_os_name": "linux centos"
        },
        {
            "bk_host_innerip": "10.0.2.7",
            "bk_os_name": "linux centos"
        },
        {
            "bk_host_innerip": "10.0.2.16",
            "bk_os_name": "linux centos"
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
    "script_data": [
        {
            "name": "获取占用内存资源最多的10个进程",
            "content": "ps aux|head -1;ps aux|grep -v PID|sort -rn -k +4|head"
        },
        {
            "name": "显示内存使用情况(以M为单位)",
            "content": "free -m"
        }
    ]
    }
    """
    # 调用开发的云API接口
    client = get_client_by_request(request)

    # 获取主机信息
    host_querysets = get_host_data(client)
    host_serializer = HostInfoSerializer(host_querysets, many=True)

    # 获取业务信息
    business_querysets = get_business_data(client)
    business_serializer = BusinessInfoSerializer(business_querysets, many=True)

    # 获取脚本信息
    script_querysets = ScriptSearch.objects.all()
    script_serializer = ScriptSearchSerializer(script_querysets, many=True)

    # 返回数据
    return JsonResponse(
        {
            "host_data": host_serializer.data,
            "business_data": business_serializer.data,
            "script_data": script_serializer.data
        },
        status=200,
        safe=False
    )


@action(methods=['get'], detail=False)
def query_host_info(request):
    """
        @api {GET} /query_host_info/ 根据业务查询对应的主机信息
        @apiName queryHostInfo

        @apiParam {String} bk_biz_id         业务ID

        @apiSuccess {Array} bk_os_name       主机名称
        @apiSuccess {Array} bk_host_innerip  主机IP

        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "host_data": {
                "message": "success",
                "code": 0,
                "data": {
                    "count": 2,
                    "info": [
                        {
                            "host": {
                                "bk_cpu": 8,
                                "bk_isp_name": null,
                                "bk_os_name": "linux centos",
                                "bk_province_name": null,
                                "bk_host_id": 4,
                                "import_from": "2",
                                "bk_os_version": "7.6.1810",
                                "bk_disk": 245,
                                "operator": null,
                                "create_time": "2019-10-11T19:09:03.441+08:00",
                                "bk_mem": 32011,
                                "bk_host_name": "VM_2_15_centos",
                                "last_time": "2020-01-02T11:56:52.812+08:00",
                                "bk_host_innerip": "10.0.2.15",
                                "bk_comment": "",
                                "bk_os_bit": "64-bit",
                                "bk_outer_mac": "",
                                "bk_asset_id": "",
                                "bk_service_term": null,
                                "bk_cloud_id": [
                                    {
                                        "bk_obj_name": "",
                                        "id": "0",
                                        "bk_obj_id": "plat",
                                        "bk_obj_icon": "",
                                        "bk_inst_id": 0,
                                        "bk_inst_name": "default area"
                                    }
                                ],
                                "bk_sla": null,
                                "bk_cpu_mhz": 1999,
                                "bk_host_outerip": "",
                                "bk_state_name": null,
                                "bk_os_type": "1",
                                "bk_mac": "52:54:00:dc:c6:a3",
                                "bk_bak_operator": null,
                                "bk_supplier_account": "0",
                                "bk_sn": "",
                                "bk_cpu_module": "AMD EPYC Processor"
                            },
                            "set": [],
                            "biz": [],
                            "module": []
                        },
                        {
                            "host": {
                                "bk_cpu": 8,
                                "bk_isp_name": null,
                                "bk_os_name": "linux centos",
                                "bk_province_name": null,
                                "bk_host_id": 5,
                                "import_from": "2",
                                "bk_os_version": "7.6.1810",
                                "bk_disk": 245,
                                "operator": null,
                                "create_time": "2019-10-11T19:09:07.77+08:00",
                                "bk_mem": 32011,
                                "bk_host_name": "VM_2_8_centos",
                                "last_time": "2019-10-24T15:08:32.424+08:00",
                                "bk_host_innerip": "10.0.2.8",
                                "bk_comment": "",
                                "bk_os_bit": "64-bit",
                                "bk_outer_mac": "",
                                "bk_asset_id": "",
                                "bk_service_term": null,
                                "bk_cloud_id": [
                                    {
                                        "bk_obj_name": "",
                                        "id": "0",
                                        "bk_obj_id": "plat",
                                        "bk_obj_icon": "",
                                        "bk_inst_id": 0,
                                        "bk_inst_name": "default area"
                                    }
                                ],
                                "bk_sla": null,
                                "bk_cpu_mhz": 1996,
                                "bk_host_outerip": "",
                                "bk_state_name": null,
                                "bk_os_type": "1",
                                "bk_mac": "52:54:00:0e:46:0d",
                                "bk_bak_operator": null,
                                "bk_supplier_account": "0",
                                "bk_sn": "",
                                "bk_cpu_module": "AMD EPYC Processor"
                            },
                            "set": [],
                            "biz": [],
                            "module": []
                        }
                    ]
                },
                "result": true,
                "request_id": "027ec3906a6542118564bd7054d3bd85"
            }
        }
    """
    client = get_client_by_request(request)
    host_data = client.cc.search_host({"bk_biz_id": request.GET.get("bk_biz_id", "")})
    return JsonResponse({"host_data": host_data})


@csrf_exempt
@action(methods=['post'], detail=False)
def execute_script(request):
    """
        @api {GET} /execute_script/ 执行脚本
        @apiName executeScript

        @apiParam {String} user              用户名
        @apiParam {String} bk_biz_id         业务ID
        @apiParam {String} script            要执行的脚本
        @apiParam {String} host_ips          要执行脚本的主机IP列表

        @apiSuccess {Integer} condition       是否执行成功

        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "message": "success",
            "condition": true,
            "data": {}
        }
    """
    return handle_execute_script(request)


class ScriptJobRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScriptJobRecord.objects.all()
    serializer_class = ScriptJobRecordSerializer

    def list(self, request, *args, **kwargs):
        """
        @api {GET} /records/ 获取任务的执行记录
        @apiName queryRecord

        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        [
            {
                "business": "测试业务",
                "mission": "获取占用内存资源最多的10个进程",
                "operator": "1819785416",
                "start_time": "2020-06-01T14:50:58.007926",
                "machine_num": 2,
                "status": "True"
            },
            {
                "business": "蓝鲸",
                "mission": "获取占用内存资源最多的10个进程",
                "operator": "admin",
                "start_time": "2020-06-01T14:51:10.940587",
                "machine_num": 1,
                "status": "False"
            },
            {
                "business": "蓝鲸",
                "mission": "获取占用内存资源最多的10个进程",
                "operator": "1819785416",
                "start_time": "2020-06-01T14:51:58.829762",
                "machine_num": 1,
                "status": "False"
            }
        ]
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        @api {GET} /records/retrieve/ 筛选数据记录
        @apiName queryRecord

        @apiParam {String} business 业务
        @apiParam {String} operator 操作者
        @apiParam {String} mission 任务

        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        [
            {
                "business": "蓝鲸",
                "mission": "获取占用内存资源最多的10个进程",
                "operator": "admin",
                "start_time": "2020-06-01T14:51:10.940587",
                "machine_num": 1,
                "status": "False"
            },
            {
                "business": "蓝鲸",
                "mission": "获取占用内存资源最多的10个进程",
                "operator": "1819785416",
                "start_time": "2020-06-01T14:51:58.829762",
                "machine_num": 1,
                "status": "False"
            },
            {
                "business": "蓝鲸",
                "mission": "获取占用内存资源最多的10个进程",
                "operator": "admin",
                "start_time": "2020-06-01T14:53:43.580829",
                "machine_num": 1,
                "status": "False"
            },
            {
                "business": "蓝鲸",
                "mission": "获取占用内存资源最多的10个进程",
                "operator": "1819785416",
                "start_time": "2020-06-01T14:53:57.705680",
                "machine_num": 1,
                "status": "False"
            },
            {
                "business": "蓝鲸",
                "mission": "获取占用内存资源最多的10个进程",
                "operator": "1819785416",
                "start_time": "2020-06-01T14:58:12.894792",
                "machine_num": 1,
                "status": "False"
            },
            {
                "business": "蓝鲸",
                "mission": "获取占用内存资源最多的10个进程",
                "operator": "1819785416",
                "start_time": "2020-06-01T15:04:05.379555",
                "machine_num": 1,
                "status": "False"
            },
            {
                "business": "蓝鲸",
                "mission": "获取占用内存资源最多的10个进程",
                "operator": "admin",
                "start_time": "2020-06-01T15:07:27.456448",
                "machine_num": 1,
                "status": "False"
            }
        ]
        """
        kwargs = pkg_retrieve_kwargs(request)
        instance = ScriptJobRecord.objects.filter(**kwargs)
        serializer = ScriptJobRecordSerializer(instance, many=True)
        return Response(serializer.data)
