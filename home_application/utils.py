# _*_ coding: utf-8 _*_
import json

from blueking.component.client import ComponentClient
from blueking.component.shortcuts import get_client_by_request

from home_application.models import Host, Business, LoginBkToken


def get_bk_token_by_request(request):
    li_cookie = request.headers["Cookie"].split(";")
    for cookie_item in li_cookie:
        if "bk_token" in cookie_item:
            return cookie_item.split("=")[1]


def save_bk_token_to_db(request):
    """把调用第三方接口需要的信息存入数据库中，方便后期调用
    """
    bk_token = request.headers["Cookie"].split(";")[0].split("=")[1]
    try:
        queryset = LoginBkToken.objects.first()
        if queryset:
            LoginBkToken.objects.update_or_create(pk=queryset.id, defaults={"bk_token": bk_token})
        else:
            LoginBkToken.objects.create(bk_token=bk_token)
    except Exception:
        pass


def get_client(bk_token):
    return ComponentClient(
            app_code="herokingfsaas",
            app_secret="d9664192-989a-424e-b0e6-5acb404fee2d",
            common_args={"bk_token": bk_token}
        )


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')

        return json.JSONEncoder.default(self, obj)


def update_host_db(to_host_db_data, bk_biz_id):
    """将主机信息更新到数据库
    """
    latest_data = []
    for item in to_host_db_data:
        kwargs = {
            "bk_cloud_id": item["host"]["bk_cloud_id"][0]["id"],
            "bk_biz_id": bk_biz_id,
            "bk_host_id": item["host"].get("bk_host_id", ""),
            "bk_host_innerip": item["host"].get("bk_host_innerip", "")
        }
        latest_data.append(kwargs)
        Host.objects.update_or_create(**kwargs, defaults={
            "bk_cloud_id": item["host"]["bk_cloud_id"][0]["id"],
            "bk_biz_id": bk_biz_id,
            "bk_cpu": item["host"].get("bk_cpu", ""),
            "bk_os_name": item["host"].get("bk_os_name", ""),
            "bk_host_id": item["host"].get("bk_host_id", ""),
            "bk_host_innerip": item["host"].get("bk_host_innerip", ""),
            "bk_os_bit": item["host"].get("bk_os_bit", "")
        })

    # 删除不在查询到的数据中的数据
    querysets = Host.objects.values("bk_cloud_id", "bk_biz_id", "bk_host_innerip", "bk_host_id")
    for item in querysets:
        if item.get("bk_biz_id") == bk_biz_id and item not in latest_data:
            Host.objects.filter(**item).delete()


def update_business_db(to_business_db_data):
    """
    查询业务信息（第一次查询的时候，需要调用配置平台的接口获取业务信息并存入数据库）
    """
    latest_data = []
    for index, item in enumerate(to_business_db_data):
        kwargs = {
            "bk_biz_id": item.get("bk_biz_id", ""),
            "bk_biz_name": item.get("bk_biz_name", "")
        }
        Business.objects.update_or_create(**kwargs, defaults=kwargs)
        latest_data.append(kwargs)

    # 删除不在查询到的数据中的数据
    querysets = Business.objects.values("bk_biz_id", "bk_biz_name")
    for item in querysets:
        if item not in latest_data:
            Business.objects.filter(**item).delete()
