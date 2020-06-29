# -*- coding: utf-8 -*-
from django.db import models


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
        ("1", "未执行"),
        ("2", "正在执行"),
        ("3", "执行成功"),
        ("4", "执行失败"),
        ("5", "跳过"),
        ("6", "忽略错误"),
        ("7", "等待用户"),
        ("8", "手动结束"),
        ("9", "状态异常"),
        ("10", "步骤强制终止中"),
        ("11", "步骤强制终止成功"),
        ("12", "步骤强制终止失败"),
        ("13", "提交失败")
    )
    business_name = models.CharField(verbose_name="业务名称", max_length=128)
    mission_name = models.CharField(verbose_name="任务名称", max_length=128)
    machine_num = models.IntegerField(verbose_name="机器数")
    status = models.CharField(verbose_name="执行状态", choices=JOB_STATUS, max_length=32, default="1")
    job_instance_id = models.IntegerField(verbose_name="任务实例ID", null=True, blank=True)
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


class Business(models.Model):
    """
    获取业务信息
    """
    bk_biz_id = models.IntegerField(verbose_name="业务ID")
    bk_biz_name = models.CharField(verbose_name="业务名称", max_length=128)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    last_edit_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "business"
        verbose_name = "业务信息"
        verbose_name_plural = verbose_name


class Host(models.Model):
    """
    存储主机信息
    调用第三放接口返回的数据中，"核数" 和 ”操作系统名称“字段可能为空，所以暂时让该字段可为空
    """
    bk_cloud_id = models.CharField(verbose_name="云区域ID", max_length=32)
    bk_biz_id = models.IntegerField(verbose_name="所属业务的ID")
    bk_cpu = models.IntegerField(verbose_name="核数", null=True, blank=True)
    bk_os_name = models.CharField(verbose_name="操作系统名称", max_length=32, null=True, blank=True)
    bk_host_id = models.IntegerField(verbose_name="主机ID")
    bk_host_innerip = models.CharField(verbose_name="内网IP", max_length=32)
    bk_os_bit = models.CharField(verbose_name="位数", max_length=8)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    last_edit_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "host"
        verbose_name = "主机信息"
        verbose_name_plural = verbose_name


class BkToken(models.Model):
    """
    存储celery周期任务中需要的client信息
    """
    bk_token = models.TextField(verbose_name="登录用户的bk_token")

    class Meta:
        db_table = "bk_token"
        verbose_name = "bk_token"
        verbose_name_plural = verbose_name


class QueryParams(models.Model):
    bk_biz_id = models.CharField(verbose_name="业务ID", max_length=16)
    job_instance_id = models.IntegerField(verbose_name="任务实例ID")
    record_id = models.IntegerField(verbose_name="记录的ID")

    class Meta:
        db_table = "query_param"
        verbose_name = "查询任务的参数"
        verbose_name_plural = verbose_name
