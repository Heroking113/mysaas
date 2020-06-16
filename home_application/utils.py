# _*_ coding: utf-8 _*_
import json

from blueking.component.shortcuts import get_client_by_request

from home_application.models import MissionRecord
from home_application.task import async_handle_execute_script


def handle_execute_script(request):
    """
    将任务信息记录到数据库，并通过异步任务执行脚本，将执行状态更新到数据库
    """
    client = get_client_by_request(request)
    bk_biz_id = request.POST.get("bk_biz_id", "")
    host_list = json.loads(request.POST.get("host_list", []))
    user = request.user.username
    business_name = request.POST.get("business_name", "")
    mission_name = request.POST.get("mission_name", "")

    ip_list = [{"bk_cloud_id": int(item["bk_cloud_id"]), "ip": item["ip"]} for item in host_list]
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
    async_result = async_handle_execute_script.delay(client, kwargs, record_id=queryset.id)
    if async_result.ready():
        res = async_result.get()
    else:
        res = "doing"

    return res
