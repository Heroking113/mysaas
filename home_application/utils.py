# _*_ coding: utf-8 _*_

from home_application.models import FastExecuteScript, ScriptSearch, ScriptJobRecord


def pkg_execute_script_kwargs(kwargs, client):
    bk_biz_id = kwargs.get("bk_biz_id", "")

    # 根据前端传来的host_ips获取bk_cloud_id
    host_data = client.cc.search_host({"bk_biz_id": bk_biz_id})["data"]["info"]
    bk_cloud_id = []
    host_ips = kwargs.get("host_ips", [])
    for host_item in host_data:
        if host_item["host"]["bk_host_innerip"] in host_ips:
            bk_cloud_id.append(host_item["host"]["bk_cloud_id"][0]["id"])
            break

    bk_cloud_id = ",".join(bk_cloud_id)
    # 把要执行的相关信息存入数据表
    fastexecutescript = FastExecuteScript.objects.create(
        bk_biz_id=bk_biz_id,
        bk_cloud_id=bk_cloud_id,
        bk_host_ip=host_ips
    )
    bk_cloud_id = bk_cloud_id.split(",")
    host_ips = host_ips.split(",")
    ip_list = [{"bk_cloud_id": bk_cloud_id[i], "ip": host_ips[i]} for i in range(len(bk_cloud_id))]

    # 获取查询脚本
    # to_execute_script = ScriptSearch.objects.get(content=kwargs["script"])
    # script_content = to_execute_script.content
    business_data = client.cc.search_business()["data"]["info"]

    bk_biz_name = None
    for business_item in business_data:
        if business_item["bk_biz_id"] == int(kwargs["bk_biz_id"]):
            bk_biz_name = business_item["bk_biz_name"]
            break
    script_job_record = ScriptJobRecord.objects.create(
        business=bk_biz_name,
        mission=kwargs["script"],
        operator=kwargs["user"],
        machine_num=len(host_ips)
    )
    record_id = script_job_record.id
    # 拼接参数
    fast_kwargs = {
        "account": "root",
        "bk_biz_id": bk_biz_id,
        "script_id": 116,
        "ip_list": ip_list,
        "record_id": record_id
    }

    return fast_kwargs


def handle_query_records():
    queryset = ScriptJobRecord.objects.all()
    users = []
    businesses = []
    missions = []
    records = []
    for item in queryset:
        dic_data = {
            "operator": item.operator,
            "business": item.business,
            "mission": item.mission,
            "start_time": item.start_time,
            "machine_num": item.machine_num,
            "status": item.status
        }
        records.append(dic_data)

    for item in records:
        users.append(item.get("operator"))
        businesses.append(item.get("business"))
        missions.append(item.get("mission"))
    users = list(set(users))
    users.append("所有用户")
    users.reverse()
    businesses = list(set(businesses))
    businesses.append("所有业务")
    businesses.reverse()
    missions = list(set(missions))
    missions.append("所有任务")
    missions.reverse()

    return {
            "users": users,
            "businesses": businesses,
            "missions": missions,
            "all_info": records
        }
