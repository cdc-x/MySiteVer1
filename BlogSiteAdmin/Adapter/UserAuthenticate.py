from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from UserManage.models import *
import datetime


class UserAuthentication(BaseAuthentication):

    def authenticate(self, request):
        ret_data = {"status_code": 1002, "msg": ""}
        token = request.META.get("HTTP_AUTHORIZATION", "")

        user_obj = UserInfo.objects.filter(token=token).first()

        if user_obj:
            last_login_time = user_obj.last_login_time
            current_time = datetime.datetime.now()

            delta = (current_time - last_login_time).total_seconds()

            if delta > 86400:
                ret_data["msg"] = "登录已超时"
                raise AuthenticationFailed(ret_data)
        else:
            ret_data["msg"] = "用户未登录"
            raise AuthenticationFailed(ret_data)

        ret = (user_obj.id, token)

        return ret
