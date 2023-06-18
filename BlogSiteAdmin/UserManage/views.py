import time
import logging
import datetime
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from Adapter.PassWordEncrypt import DES3
from utils.common import encrypt_str

logger = logging.getLogger("log")


class UserLoginView(APIView):
    """
    用户登录
    """
    authentication_classes = []

    @staticmethod
    def post(request):
        try:
            user_info = request.data
            username = user_info.get("userName", "")
            pwd_encrypt = user_info.get("passWord", "")

            # 对密码进行解密
            des = DES3()
            pwd_decrypt = des.des3_decrypt(pwd_encrypt)

            # 对密码进行hash加密
            pwd_hash = encrypt_str(pwd_decrypt, pwd_decrypt)

            # 查询用户信息是否存在
            user_obj = UserInfo.objects.filter(username=username, password=pwd_hash).first()

            if user_obj:
                user_obj.last_login_time = datetime.datetime.now().replace(microsecond=0)
                user_obj.token = encrypt_str(username, str(time.time()))
                user_obj.save()

                user_message = {
                    "username": user_obj.username,
                    "last_login_time": user_obj.last_login_time,
                    "uid": user_obj.id,
                    "token": user_obj.token
                }

                ret_data = {"status_code": 1000, "message": "登陆成功", "data": user_message}
                logger.info(f"【用户登录】-【{username}】-【成功】")
            else:
                ret_data = {"status_code": 1001, "message": "用户名或密码不正确"}
                logger.error(f"【用户登录】-【{username}】-【失败】-【用户名或密码不正确】")
        except Exception as e:
            logger.error(f"【用户登录】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class UserLogoutView(APIView):

    @staticmethod
    def get(request):
        try:
            user_id = request.user
            UserInfo.objects.filter(id=user_id).update(token="")
            logger.info(f"【用户退出】- 【成功】-【{user_id}】")
            ret_data = {"status_code": 1000, "message": "退出登录成功"}
        except Exception as e:
            logger.error(f"【用户退出】- 【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": "退出登录失败"}

        return Response(ret_data)


class AddUserView(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            username = data.get("userName", "")

            # 查询用户是否已存在
            query = UserInfo.objects.filter(username=username)
            if query:
                ret_data = {"status_code": 1001, "message": "用户已存在"}
                logger.error(f"【新增用户】- 【失败】-【{username}】-【用户已存在】")
            else:
                user_data = {
                    "username": username,
                    "password": encrypt_str(data["passWord"], data["passWord"]),
                    "last_login_time": datetime.datetime.now().replace(microsecond=0)
                }

                print(user_data)

                serializer = UserInfoSerializer(data=user_data)

                if serializer.is_valid():
                    serializer.save()
                    ret_data = {"status_code": 1000, "message": "新增用户成功", "data": serializer.data}
                    logger.info(f"【新增用户】- 【成功】-【{username}】")
                else:
                    ret_data = {"status_code": 1001, "message": serializer.errors}
                    logger.error(f"【新增用户】- 【失败】-【{username}】- {str(serializer.errors)}")
        except Exception as e:
            logger.error(f"【新增用户】- 【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)
