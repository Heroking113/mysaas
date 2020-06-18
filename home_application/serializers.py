# _*_ coding: utf-8 _*_

from rest_framework import serializers

from home_application.models import MissionRecord, Host, Mission, Business


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = "__all__"


class MissionRecordSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = MissionRecord
        fields = "__all__"

    def get_status(self, obj):
        return obj.get_status_display()


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = "__all__"


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = "__all__"
