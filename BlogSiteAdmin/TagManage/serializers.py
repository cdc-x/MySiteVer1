from rest_framework import serializers
from .models import *


class TagSerializer(serializers.ModelSerializer):
    create__time = serializers.SerializerMethodField()
    update__time = serializers.SerializerMethodField()

    @staticmethod
    def get_create__time(obj):
        if obj.create_time:
            return obj.create_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ""

    @staticmethod
    def get_update__time(obj):
        if obj.update_time:
            return obj.update_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ""

    class Meta:
        model = Tag
        fields = "__all__"
