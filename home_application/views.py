# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet

from blueking.component.shortcuts import get_client_by_request

from home_application.models import HostInfo, BusinessInfo, MissionInfo
from home_application.serializers import HostInfoSerializer, BusinessInfoSerializer, MissionInfoSerializer
from home_application.common import CustomResponse, get_cc_hosts


def index(request):
    """
    前后端分离模式:跳转到前端首页
    """
    return render(request, "index.html")


# class RetrieveHostInfoViewSet(viewsets.ViewSet):
#     """用基于类的视图实现对主机信息的筛选"""
#     def retrieve(self, request, pk=None):
#         bk_biz_id = request.query_params.get("bk_biz_id", "")
#         client = get_client_by_request(request)
#         data = get_cc_hosts(client, bk_biz_id=bk_biz_id)
#
#         return CustomResponse(result=True, code=200, message="success", data=data)

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
    client = get_client_by_request(request)
    data = get_cc_hosts(client, bk_biz_id=bk_biz_id)

    return CustomResponse(result=True, code=200, message="success", data=data)


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
    client = get_client_by_request(request)
    # 获取主机信息
    host_querysets = HostInfo.query_hosts(start=0, limit=15, client=client)
    host_serializer = HostInfoSerializer(host_querysets, many=True)
    host_data = host_serializer.data

    # 获取业务信息
    business_querysets = BusinessInfo.query_businesses(start=0, limit=50, client=client)
    business_serializer = BusinessInfoSerializer(business_querysets, many=True)
    business_data = business_serializer.data

    # 获取任务信息
    mission_querysets = MissionInfo.objects.all()
    mission_serializer = MissionInfoSerializer(mission_querysets, many=True)
    mission_data = mission_serializer.data

    res_data = {
        "host_data": host_data,
        "business_data": business_data,
        "mission_data": mission_data
    }

    return CustomResponse(result=True, code=200, message="success", data=res_data)

#
#
# @action(methods=['get'], detail=False)
# def query_host_info(request):
#     """
#         @api {GET} /query_host_info/ 根据业务查询对应的主机信息
#         @apiName queryHostInfo
#
#         @apiParam {String} bk_biz_id         业务ID
#
#         @apiSuccess {Array} bk_os_name       主机名称
#         @apiSuccess {Array} bk_host_innerip  主机IP
#
#         @apiSuccess Example {json} Success-Response:
#         HTTP/1.1 200 OK
#         {
#             "host_data": {
#                 "message": "success",
#                 "code": 0,
#                 "data": {
#                     "count": 2,
#                     "info": [
#                         {
#                             "host": {
#                                 "bk_cpu": 8,
#                                 "bk_isp_name": null,
#                                 "bk_os_name": "linux centos",
#                                 "bk_province_name": null,
#                                 "bk_host_id": 4,
#                                 "import_from": "2",
#                                 "bk_os_version": "7.6.1810",
#                                 "bk_disk": 245,
#                                 "operator": null,
#                                 "create_time": "2019-10-11T19:09:03.441+08:00",
#                                 "bk_mem": 32011,
#                                 "bk_host_name": "VM_2_15_centos",
#                                 "last_time": "2020-01-02T11:56:52.812+08:00",
#                                 "bk_host_innerip": "10.0.2.15",
#                                 "bk_comment": "",
#                                 "bk_os_bit": "64-bit",
#                                 "bk_outer_mac": "",
#                                 "bk_asset_id": "",
#                                 "bk_service_term": null,
#                                 "bk_cloud_id": [
#                                     {
#                                         "bk_obj_name": "",
#                                         "id": "0",
#                                         "bk_obj_id": "plat",
#                                         "bk_obj_icon": "",
#                                         "bk_inst_id": 0,
#                                         "bk_inst_name": "default area"
#                                     }
#                                 ],
#                                 "bk_sla": null,
#                                 "bk_cpu_mhz": 1999,
#                                 "bk_host_outerip": "",
#                                 "bk_state_name": null,
#                                 "bk_os_type": "1",
#                                 "bk_mac": "52:54:00:dc:c6:a3",
#                                 "bk_bak_operator": null,
#                                 "bk_supplier_account": "0",
#                                 "bk_sn": "",
#                                 "bk_cpu_module": "AMD EPYC Processor"
#                             },
#                             "set": [],
#                             "biz": [],
#                             "module": []
#                         },
#                         {
#                             "host": {
#                                 "bk_cpu": 8,
#                                 "bk_isp_name": null,
#                                 "bk_os_name": "linux centos",
#                                 "bk_province_name": null,
#                                 "bk_host_id": 5,
#                                 "import_from": "2",
#                                 "bk_os_version": "7.6.1810",
#                                 "bk_disk": 245,
#                                 "operator": null,
#                                 "create_time": "2019-10-11T19:09:07.77+08:00",
#                                 "bk_mem": 32011,
#                                 "bk_host_name": "VM_2_8_centos",
#                                 "last_time": "2019-10-24T15:08:32.424+08:00",
#                                 "bk_host_innerip": "10.0.2.8",
#                                 "bk_comment": "",
#                                 "bk_os_bit": "64-bit",
#                                 "bk_outer_mac": "",
#                                 "bk_asset_id": "",
#                                 "bk_service_term": null,
#                                 "bk_cloud_id": [
#                                     {
#                                         "bk_obj_name": "",
#                                         "id": "0",
#                                         "bk_obj_id": "plat",
#                                         "bk_obj_icon": "",
#                                         "bk_inst_id": 0,
#                                         "bk_inst_name": "default area"
#                                     }
#                                 ],
#                                 "bk_sla": null,
#                                 "bk_cpu_mhz": 1996,
#                                 "bk_host_outerip": "",
#                                 "bk_state_name": null,
#                                 "bk_os_type": "1",
#                                 "bk_mac": "52:54:00:0e:46:0d",
#                                 "bk_bak_operator": null,
#                                 "bk_supplier_account": "0",
#                                 "bk_sn": "",
#                                 "bk_cpu_module": "AMD EPYC Processor"
#                             },
#                             "set": [],
#                             "biz": [],
#                             "module": []
#                         }
#                     ]
#                 },
#                 "result": true,
#                 "request_id": "027ec3906a6542118564bd7054d3bd85"
#             }
#         }
#     """
#     client = get_client_by_request(request)
#     host_data = client.cc.search_host({"bk_biz_id": request.GET.get("bk_biz_id", "")})
#     return JsonResponse({"host_data": host_data})
#
#
# @csrf_exempt
# @action(methods=['post'], detail=False)
# def execute_script(request):
#     """
#         @api {GET} /execute_script/ 执行脚本
#         @apiName executeScript
#
#         @apiParam {String} user              用户名
#         @apiParam {String} bk_biz_id         业务ID
#         @apiParam {String} script            要执行的脚本
#         @apiParam {String} host_ips          要执行脚本的主机IP列表
#
#         @apiSuccess {Integer} condition       是否执行成功
#
#         @apiSuccess Example {json} Success-Response:
#         HTTP/1.1 200 OK
#         {
#             "message": "success",
#             "condition": true,
#             "data": {}
#         }
#     """
#     return handle_execute_script(request)
#
#
# class ScriptJobRecordViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = ScriptJobRecord.objects.all()
#     serializer_class = ScriptJobRecordSerializer
#
#     def list(self, request, *args, **kwargs):
#         """
#         @api {GET} /records/ 获取任务的执行记录
#         @apiName queryRecord
#
#         @apiSuccess Example {json} Success-Response:
#         HTTP/1.1 200 OK
#         [
#             {
#                 "business": "测试业务",
#                 "mission": "获取占用内存资源最多的10个进程",
#                 "operator": "1819785416",
#                 "start_time": "2020-06-01T14:50:58.007926",
#                 "machine_num": 2,
#                 "status": "True"
#             },
#             {
#                 "business": "蓝鲸",
#                 "mission": "获取占用内存资源最多的10个进程",
#                 "operator": "admin",
#                 "start_time": "2020-06-01T14:51:10.940587",
#                 "machine_num": 1,
#                 "status": "False"
#             },
#             {
#                 "business": "蓝鲸",
#                 "mission": "获取占用内存资源最多的10个进程",
#                 "operator": "1819785416",
#                 "start_time": "2020-06-01T14:51:58.829762",
#                 "machine_num": 1,
#                 "status": "False"
#             }
#         ]
#         """
#         return super().list(request, *args, **kwargs)
#
#     def retrieve(self, request, *args, **kwargs):
#         """
#         @api {GET} /records/retrieve/ 筛选数据记录
#         @apiName queryRecord
#
#         @apiParam {String} business 业务
#         @apiParam {String} operator 操作者
#         @apiParam {String} mission 任务
#
#         @apiSuccess Example {json} Success-Response:
#         HTTP/1.1 200 OK
#         [
#             {
#                 "business": "蓝鲸",
#                 "mission": "获取占用内存资源最多的10个进程",
#                 "operator": "admin",
#                 "start_time": "2020-06-01T14:51:10.940587",
#                 "machine_num": 1,
#                 "status": "False"
#             },
#             {
#                 "business": "蓝鲸",
#                 "mission": "获取占用内存资源最多的10个进程",
#                 "operator": "1819785416",
#                 "start_time": "2020-06-01T14:51:58.829762",
#                 "machine_num": 1,
#                 "status": "False"
#             }
#         ]
#         """
#         kwargs = pkg_retrieve_kwargs(request)
#         instance = ScriptJobRecord.objects.filter(**kwargs)
#         serializer = ScriptJobRecordSerializer(instance, many=True)
#         return Response(serializer.data)
