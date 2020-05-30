# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class ScriptSearch(models.Model):
    name = models.CharField(max_length=100, default='')
    content = models.CharField(max_length=300, default='')


class FastExecuteScript(models.Model):
    bk_biz_id = models.CharField(max_length=100, default="")
    bk_cloud_id = models.CharField(max_length=100, default="")
    bk_host_innerip = models.CharField(max_length=100, default="")
