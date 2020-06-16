# _*_ coding: utf-8 _*_

from rest_framework import serializers

from home_application.models import MissionRecord


class MissionInfoSerializer(serializers.Serializer):
    mission_name = serializers.CharField(required=True)
    mission_content = serializers.CharField(required=True)


class MissionRecordSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = MissionRecord
        fields = "__all__"

    def get_status(self, obj):
        return obj.get_status_display()


class HostInfoSerializer(serializers.Serializer):
    bk_cloud_id = serializers.CharField(required=True)
    bk_cpu = serializers.IntegerField(required=True)
    bk_os_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    bk_host_id = serializers.CharField(required=True)
    bk_host_innerip = serializers.CharField(required=True)
    bk_os_bit = serializers.CharField(required=True)
    create_time = serializers.DateTimeField(required=True)


class BusinessInfoSerializer(serializers.Serializer):
    bk_biz_id = serializers.CharField(required=True)
    bk_biz_name = serializers.CharField(required=True)
