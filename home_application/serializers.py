# _*_ coding: utf-8 _*_

from rest_framework import serializers


class ScriptSearchSerializer(serializers.Serializer):
    name =serializers.CharField(read_only=True)
    content = serializers.CharField(read_only=True)