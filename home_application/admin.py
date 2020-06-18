# -*- coding: utf-8 -*-
from django.contrib import admin

from home_application.models import Mission, MissionRecord, Host, Business


# Register your models here.
@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('mission_name', 'mission_content')


@admin.register(MissionRecord)
class MissionRecordAdmin(admin.ModelAdmin):
    list_display = ("business_name", "mission_name", "status", "operator", "create_time")


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ("bk_cloud_id", "bk_cpu", "bk_os_name", "bk_host_id", "bk_host_innerip", "create_time")


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("bk_biz_id", "bk_biz_name")
