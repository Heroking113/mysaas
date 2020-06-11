# -*- coding: utf-8 -*-
from django.contrib import admin

from home_application.models import MissionInfo, MissionRecord, HostInfo, BusinessInfo


# Register your models here.
@admin.register(MissionInfo)
class MissionInfoAdmin(admin.ModelAdmin):
    list_display = ('mission_name', 'mission_content')


@admin.register(MissionRecord)
class MissionRecordAdmin(admin.ModelAdmin):
    list_display = ("business_name", "mission_name", "status", "operator", "create_time")


@admin.register(HostInfo)
class HostInfoAdmin(admin.ModelAdmin):
    list_display = ("bk_cloud_id", "bk_cpu", "bk_os_name", "bk_host_id", "bk_host_innerip", "create_time")


@admin.register(BusinessInfo)
class BusinessInfoAdmin(admin.ModelAdmin):
    list_display = ("bk_biz_id", "bk_biz_name")
