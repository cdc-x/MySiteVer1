from rest_framework import serializers
from .models import *


class UserInfoSerializer(serializers.ModelSerializer):
    last_login_time = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_last_login_time(obj):
        if not obj.last_login_time:
            return ""

        return obj.last_login_time.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserInfo
        fields = "__all__"
