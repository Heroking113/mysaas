# -*- coding: utf-8 -*-
from unittest.mock import patch, Mock
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from home_application import views


class QueryAllInfoTest(APITestCase):
    """
    查询所有基础数据的测试类
    """
    def setUp(self):
        self.host_info = {
            "errors": None,
            "message": "ok",
            "code": "1500200",
            "data": {
                "count": 3,
                "info": [
                    {
                        "host": {
                            "bk_cpu": 12,
                            "bk_isp_name": None,
                            "bk_os_name": "linux centos",
                            "bk_province_name": None,
                            "bk_host_id": 4,
                            "import_from": "3",
                            "bk_os_version": "7.6.1810",
                            "bk_disk": 98,
                            "operator": None,
                            "docker_server_version": "",
                            "create_time": "2019-11-29T09:56:14.68+08:00",
                            "bk_mem": 48137,
                            "bk_host_name": "bkdata-dataflowapi-1",
                            "last_time": "2020-05-22T17:15:31.462+08:00",
                            "bk_host_innerip": "10.0.5.247",
                            "bk_comment": "",
                            "docker_client_version": "",
                            "bk_os_bit": "64-bit",
                            "bk_outer_mac": "",
                            "bk_asset_id": "",
                            "bk_service_term": None,
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
                            "bk_sla": None,
                            "bk_cpu_mhz": 2399,
                            "bk_host_outerip": "",
                            "bk_sn": "",
                            "bk_os_type": "1",
                            "bk_mac": "52:54:00:a2:02:ac",
                            "bk_bak_operator": None,
                            "bk_supplier_account": "0",
                            "bk_state_name": None,
                            "bk_cpu_module": "Intel(R) Xeon(R) CPU E5-26xx v4"
                        },
                        "set": [],
                        "biz": [],
                        "module": []
                    },
                    {
                        "host": {
                            "bk_cpu": 12,
                            "bk_isp_name": None,
                            "bk_os_name": "linux centos",
                            "bk_province_name": None,
                            "bk_host_id": 5,
                            "import_from": "3",
                            "bk_os_version": "7.6.1810",
                            "bk_disk": 98,
                            "operator": None,
                            "docker_server_version": "",
                            "create_time": "2019-11-29T09:57:15.401+08:00",
                            "bk_mem": 48137,
                            "bk_host_name": "hadoop-resourcemanager-2",
                            "last_time": "2020-05-22T17:15:31.475+08:00",
                            "bk_host_innerip": "10.0.5.234",
                            "bk_comment": "",
                            "docker_client_version": "",
                            "bk_os_bit": "64-bit",
                            "bk_outer_mac": "",
                            "bk_asset_id": "",
                            "bk_service_term": None,
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
                            "bk_sla": None,
                            "bk_cpu_mhz": 2294,
                            "bk_host_outerip": "",
                            "bk_sn": "",
                            "bk_os_type": "1",
                            "bk_mac": "52:54:00:24:5c:85",
                            "bk_bak_operator": None,
                            "bk_supplier_account": "0",
                            "bk_state_name": None,
                            "bk_cpu_module": "Intel(R) Xeon(R) CPU E5-26xx v3"
                        },
                        "set": [],
                        "biz": [],
                        "module": []
                    },
                    {
                        "host": {
                            "bk_cpu": 12,
                            "bk_isp_name": None,
                            "bk_os_name": "linux centos",
                            "bk_province_name": None,
                            "bk_host_id": 8,
                            "import_from": "3",
                            "bk_os_version": "7.6.1810",
                            "bk_disk": 541,
                            "operator": None,
                            "docker_server_version": "",
                            "create_time": "2019-12-11T14:18:31.124+08:00",
                            "bk_mem": 48137,
                            "bk_host_name": "VM_5_7_centos",
                            "last_time": "2020-05-22T17:15:31.488+08:00",
                            "bk_host_innerip": "10.0.5.7",
                            "bk_comment": "",
                            "docker_client_version": "",
                            "bk_os_bit": "64-bit",
                            "bk_outer_mac": "",
                            "bk_asset_id": "",
                            "bk_service_term": None,
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
                            "bk_sla": None,
                            "bk_cpu_mhz": 2394,
                            "bk_host_outerip": "",
                            "bk_sn": "",
                            "bk_os_type": "1",
                            "bk_mac": "52:54:00:f8:c9:16",
                            "bk_bak_operator": None,
                            "bk_supplier_account": "0",
                            "bk_state_name": None,
                            "bk_cpu_module": "Intel(R) Xeon(R) CPU E5-26xx v3"
                        },
                        "set": [],
                        "biz": [],
                        "module": []
                    }
                ]
            },
            "result": True
        }
        self.business_info = {
            "message": "success",
            "code": 0,
            "data":
                {
                    "count": 4,
                    "info": [
                        {
                            "bk_biz_id": 2,
                            "create_time": "2019-10-11T19:06:19.412+08:00",
                            "bk_biz_name": "蓝鲸"
                        }, {
                            "bk_biz_id": 3,
                            "create_time": "2019-10-11T20:10:02.635+08:00",
                            "bk_biz_name": "测试业务"
                        }, {
                            "bk_biz_id": 5,
                            "create_time": "2020-02-13T16:34:34.912+08:00",
                            "bk_biz_name": "流程管理服务"
                        }, {
                            "bk_biz_id": 6,
                            "create_time": "2020-04-21T15:58:54.745+08:00",
                            "bk_biz_name": "实验专用业务",
                        }
                    ]
                },
            "result": True,
            "request_id": "043c23b5274442cc831d8f1501f264f3"
        }

    @patch("home_application.views.get_client_by_request")
    def test_success_case(self, mocked_get_client_by_request):
        """
        获取所有信息成功的测试用例
        """
        client = Mock()
        mocked_get_client_by_request.return_value = client
        client.cc.search_host.return_value = self.host_info
        client.cc.search_business.return_value = self.business_info
        url = "/query_all_info/"
        factory = APIRequestFactory()
        request = factory.get(url)
        response = views.query_all_info(request)
        self.assertEqual(response.status_code, 200)

    def test_not_login_case(self):
        """
        用户未登录的测试用例
        """
        url = "/query_all_info/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class RetrieveHostTest(APITestCase):
    """
    筛选主机的测试类
    """
    def setUp(self):
        self.host_info = {
            "errors": None,
            "message": "ok",
            "code": "1500200",
            "data": {
                "count": 3,
                "info": [
                    {
                        "host": {
                            "bk_cpu": 12,
                            "bk_isp_name": None,
                            "bk_os_name": "linux centos",
                            "bk_province_name": None,
                            "bk_host_id": 4,
                            "import_from": "3",
                            "bk_os_version": "7.6.1810",
                            "bk_disk": 98,
                            "operator": None,
                            "docker_server_version": "",
                            "create_time": "2019-11-29T09:56:14.68+08:00",
                            "bk_mem": 48137,
                            "bk_host_name": "bkdata-dataflowapi-1",
                            "last_time": "2020-05-22T17:15:31.462+08:00",
                            "bk_host_innerip": "10.0.5.247",
                            "bk_comment": "",
                            "docker_client_version": "",
                            "bk_os_bit": "64-bit",
                            "bk_outer_mac": "",
                            "bk_asset_id": "",
                            "bk_service_term": None,
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
                            "bk_sla": None,
                            "bk_cpu_mhz": 2399,
                            "bk_host_outerip": "",
                            "bk_sn": "",
                            "bk_os_type": "1",
                            "bk_mac": "52:54:00:a2:02:ac",
                            "bk_bak_operator": None,
                            "bk_supplier_account": "0",
                            "bk_state_name": None,
                            "bk_cpu_module": "Intel(R) Xeon(R) CPU E5-26xx v4"
                        },
                        "set": [],
                        "biz": [],
                        "module": []
                    },
                    {
                        "host": {
                            "bk_cpu": 12,
                            "bk_isp_name": None,
                            "bk_os_name": "linux centos",
                            "bk_province_name": None,
                            "bk_host_id": 5,
                            "import_from": "3",
                            "bk_os_version": "7.6.1810",
                            "bk_disk": 98,
                            "operator": None,
                            "docker_server_version": "",
                            "create_time": "2019-11-29T09:57:15.401+08:00",
                            "bk_mem": 48137,
                            "bk_host_name": "hadoop-resourcemanager-2",
                            "last_time": "2020-05-22T17:15:31.475+08:00",
                            "bk_host_innerip": "10.0.5.234",
                            "bk_comment": "",
                            "docker_client_version": "",
                            "bk_os_bit": "64-bit",
                            "bk_outer_mac": "",
                            "bk_asset_id": "",
                            "bk_service_term": None,
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
                            "bk_sla": None,
                            "bk_cpu_mhz": 2294,
                            "bk_host_outerip": "",
                            "bk_sn": "",
                            "bk_os_type": "1",
                            "bk_mac": "52:54:00:24:5c:85",
                            "bk_bak_operator": None,
                            "bk_supplier_account": "0",
                            "bk_state_name": None,
                            "bk_cpu_module": "Intel(R) Xeon(R) CPU E5-26xx v3"
                        },
                        "set": [],
                        "biz": [],
                        "module": []
                    },
                    {
                        "host": {
                            "bk_cpu": 12,
                            "bk_isp_name": None,
                            "bk_os_name": "linux centos",
                            "bk_province_name": None,
                            "bk_host_id": 8,
                            "import_from": "3",
                            "bk_os_version": "7.6.1810",
                            "bk_disk": 541,
                            "operator": None,
                            "docker_server_version": "",
                            "create_time": "2019-12-11T14:18:31.124+08:00",
                            "bk_mem": 48137,
                            "bk_host_name": "VM_5_7_centos",
                            "last_time": "2020-05-22T17:15:31.488+08:00",
                            "bk_host_innerip": "10.0.5.7",
                            "bk_comment": "",
                            "docker_client_version": "",
                            "bk_os_bit": "64-bit",
                            "bk_outer_mac": "",
                            "bk_asset_id": "",
                            "bk_service_term": None,
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
                            "bk_sla": None,
                            "bk_cpu_mhz": 2394,
                            "bk_host_outerip": "",
                            "bk_sn": "",
                            "bk_os_type": "1",
                            "bk_mac": "52:54:00:f8:c9:16",
                            "bk_bak_operator": None,
                            "bk_supplier_account": "0",
                            "bk_state_name": None,
                            "bk_cpu_module": "Intel(R) Xeon(R) CPU E5-26xx v3"
                        },
                        "set": [],
                        "biz": [],
                        "module": []
                    }
                ]
            },
            "result": True
        }

    @patch("home_application.views.get_client_by_request")
    def test_retrieve_hosts_success_case(self, mocked_get_client_by_request):
        """
        根据业务筛选主机成功的测试用例
        """
        client = Mock()
        mocked_get_client_by_request.return_value = client
        client.cc.search_host.return_value = self.host_info

        url = "/retrieve/retrieve_host/"
        factory = APIRequestFactory()
        request = factory.get(url, {"bk_biz_id": 2})
        response = views.retrieve_host(request)
        self.assertEqual(response.status_code, 200)


class ExecuteScriptTest(APITestCase):
    """
    快速执行脚本的测试类
    """
    def setUp(self):
        self.url = "/execute_script/"
        self.client = Mock()
        self.request_data = {
            "host_list": '[{"bk_cloud_id":"0","ip":"10.0.2.15"},{"bk_cloud_id":"0","ip":"10.0.2.8"}]',
            "bk_biz_id": "3",
            "encoding": "utf8",
            "business_name": "测试业务",
            "script_content": "pwd",
            "mission_name": "查看当前工作目录路径"
        }

    @patch("home_application.views.get_client_by_request")
    def test_post_execute_script_submit_success_case(self, mocked_get_client_by_request):
        """
        异步任务提交成功的测试用例
        """
        mocked_get_client_by_request.return_value = self.client
        self.client.job.fast_execute_script.return_value = {"result": True}

        factory = APIRequestFactory()
        request = factory.post(self.url, self.request_data)
        response = views.execute_script(request)
        self.assertEqual(response.status_code, 200)


class MissionRecordTest(APITestCase):
    """
    任务执行记录的测试类
    """
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_query_mission_record_success_case(self):
        """
        任务记录查询成功的测试用例
        """
        url = "/records/"
        params = {
            "business_name": "测试业务",
            "operator": "1819785416",
            "mission_name": "占用内存最高的前10个进程",
            "page": "1"
        }
        request = self.factory.get(url, params)
        view = views.MissionRecordViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_query_conditions_success_case(self):
        """
        获取任务记录的查询条件成功的测试用例
        """
        url = "/records/conditions"
        request = self.factory.get(url)
        view = views.MissionRecordViewSet.as_view({"get": "conditions"})
        response = view(request)
        self.assertEqual(response.status_code, 200)
