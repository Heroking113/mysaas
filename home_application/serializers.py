# _*_ coding: utf-8 _*_

from rest_framework import serializers

from home_application.models import ScriptJobRecord, HostInfo, BusinessInfo, ScriptSearch


class ScriptSearchSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    content = serializers.CharField(read_only=True)


class ScriptJobRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptJobRecord
        fields = ["business", "mission", "operator", "start_time", "machine_num", "status"]


class HostInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostInfo
        fields = ["bk_host_innerip", "bk_os_name"]


class BusinessInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessInfo
        fields = ["bk_biz_id", "bk_biz_name"]

