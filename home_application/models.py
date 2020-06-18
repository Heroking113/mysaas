# -*- coding: utf-8 -*-
from django.db import models

from home_application.third_party_interface import get_cc_hosts, get_cc_businesses


class Mission(models.Model):
    """存储任务信息"""
    mission_name = models.CharField(verbose_name="任务名称", max_length=128)
    mission_content = models.TextField(verbose_name="任务内容")

    class Meta:
        db_table = "mission"
        verbose_name = "任务信息"
        verbose_name_plural = verbose_name


class MissionRecord(models.Model):
    """
    任务执行记录
    """
    JOB_STATUS = (
        ("success", "执行成功"),
        ("doing", "执行中"),
        ("fail", "执行失败"),
    )
    business_name = models.CharField(verbose_name="业务名称", max_length=128)
    mission_name = models.CharField(verbose_name="任务名称", max_length=128)
    machine_num = models.IntegerField(verbose_name="机器数")
    status = models.CharField(verbose_name="执行状态", choices=JOB_STATUS, max_length=32, default="doing")
    operator = models.CharField(verbose_name="操作者", max_length=32)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "mission_record"
        verbose_name = "任务记录"
        verbose_name_plural = verbose_name

    @classmethod
    def query_records_with_condition(cls, request):
        """按条件查询任务记录"""
        business_name = request.query_params.get("business_name", "")
        mission_name = request.query_params.get("mission_name", "")
        operator = request.query_params.get("operator", "")
        kwargs = {}
        if business_name and business_name != "所有业务":
            kwargs["business_name"] = business_name
        if mission_name and mission_name != "所有任务":
            kwargs["mission_name"] = mission_name
        if operator and operator != "所有用户":
            kwargs["operator"] = operator

        querysets = cls.objects.filter(**kwargs)
        return querysets


class Host(models.Model):
    """
    存储主机信息
    调用第三放接口返回的数据中，"核数" 和 ”操作系统名称“字段可能为空，所以暂时让该字段可为空
    """
    bk_cloud_id = models.CharField(verbose_name="云区域ID", max_length=32)
    bk_cpu = models.IntegerField(verbose_name="核数", null=True, blank=True)
    bk_os_name = models.CharField(verbose_name="操作系统名称", max_length=32, null=True, blank=True)
    bk_host_id = models.IntegerField(verbose_name="主机ID")
    bk_host_innerip = models.CharField(verbose_name="内网IP", max_length=32)
    bk_os_bit = models.CharField(verbose_name="位数", max_length=8)
    create_time = models.DateTimeField(verbose_name="创建时间")

    class Meta:
        db_table = "host"
        verbose_name = "主机信息"
        verbose_name_plural = verbose_name

    @classmethod
    def query_hosts(cls, start, limit, client):
        """
        查询主机信息（第一次查询的时候，需要调用配置平台的接口获取主机信息并存入数据库）
        :param client: 调用接口的客户端
        :param start: 记录开始位置
        :param limit: 每页限制条数(最大200)
        """
        # 如果输入的 start/limit 不合法，则直接返回
        if not validate_start_limit(start, limit):
            return False
        # 查询数据库中是否有数据
        host_querysets = cls.objects.all()
        if host_querysets.exists():
            return host_querysets
        # 调用接口获取主机信息
        res_data = get_cc_hosts(client, start, limit)
        if not res_data:
            # 接口调用失败则直接返回
            return res_data
        # 解析数据，存入数据库
        host_data = []
        for item in res_data:
            host_data.append(cls(
                bk_cloud_id=item["bk_cloud_id"],
                bk_cpu=item["bk_cpu"],
                bk_os_name=item["bk_os_name"],
                bk_host_id=item["bk_host_id"],
                bk_host_innerip=item["bk_host_innerip"],
                bk_os_bit=item["bk_os_bit"],
                create_time=item["create_time"]
            ))

        # 将数据批量存入数据库，并返回
        return cls.objects.bulk_create(host_data)


class Business(models.Model):
    """
    获取业务信息
    """
    bk_biz_id = models.CharField(verbose_name="业务ID", max_length=32)
    bk_biz_name = models.CharField(verbose_name="业务名称", max_length=128)

    class Meta:
        db_table = "business"
        verbose_name = "业务信息"
        verbose_name_plural = verbose_name

    @classmethod
    def query_businesses(cls, start, limit, client):
        """
        查询业务信息（第一次查询的时候，需要调用配置平台的接口获取业务信息并存入数据库）
        :param client: 调用接口的客户端
        :param start: 记录开始位置
        :param limit: 每页限制条数(最大200)
        """
        # 如果输入的 start/limit 不合法，则直接返回
        if not validate_start_limit(start, limit):
            return False
        # 查询数据库中是否有数据
        business_querysets = cls.objects.all()
        if business_querysets.exists():
            return business_querysets
        # 调用接口获取业务信息
        res_data = get_cc_businesses(start, limit, client)
        if not res_data:
            return res_data
        # 解析数据，存入数据库
        business_data = []
        for item in res_data:
            bk_biz_id = item.get("bk_biz_id", "")
            bk_biz_name = item.get("bk_biz_name", "")
            business_data.append(Business(bk_biz_id=bk_biz_id, bk_biz_name=bk_biz_name))

        return Business.objects.bulk_create(business_data)


def validate_start_limit(start, limit):
    """验证 start 和 limit 的输入是否合法"""
    if start < 0 or limit < 0 or limit > 200:
        return False
    return True
