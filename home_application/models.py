# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class ScriptSearch(models.Model):
    name = models.CharField(max_length=100, default='')
    content = models.CharField(max_length=300, default='')


class FastExecuteScript(models.Model):
    bk_biz_id = models.CharField(max_length=100, default="")
    bk_cloud_id = models.CharField(max_length=100, default="")
    bk_host_ip = models.CharField(max_length=100, default="")


class ScriptJobRecord(models.Model):
    business = models.CharField(max_length=100, null=True, blank=True)
    mission = models.CharField(max_length=100, null=True, blank=True)
    operator = models.CharField(max_length=30, null=True, blank=True)
    start_time = models.DateTimeField(auto_now=True)
    machine_num = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)


class HostInfo(models.Model):
    bk_host_innerip = models.CharField(max_length=50, null=True, blank=True)
    bk_os_name = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = "host_info"
        verbose_name = "主机信息"
        verbose_name_plural = verbose_name


class BusinessInfo(models.Model):
    bk_biz_id = models.CharField(max_length=50, null=True, blank=True)
    bk_biz_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "business_info"
        verbose_name = "业务信息"
        verbose_name_plural = verbose_name
