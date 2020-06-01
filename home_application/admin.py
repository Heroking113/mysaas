# -*- coding: utf-8 -*-
from django.contrib import admin

from home_application.models import ScriptSearch, FastExecuteScript, ScriptJobRecord


# Register your models here.
@admin.register(ScriptSearch)
class ScriptSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')


@admin.register(FastExecuteScript)
class ScriptJobRecordAdmin(admin.ModelAdmin):
    list_display = ("bk_biz_id", "bk_cloud_id", "bk_host_ip")


@admin.register(ScriptJobRecord)
class ScriptJobRecordAdmin(admin.ModelAdmin):
    list_display = ("business", "mission", "operator", "start_time", "machine_num", "status")
