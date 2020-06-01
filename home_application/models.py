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
