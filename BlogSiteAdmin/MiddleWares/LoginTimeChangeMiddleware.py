import datetime
from django.utils.deprecation import MiddlewareMixin
from UserManage.models import UserInfo


class TimeLinesChangeMiddleware(MiddlewareMixin):

    @staticmethod
    def process_response(request, response):
        visit_path = request.path

        if visit_path.__contains__("admin") and not visit_path.__contains__("user"):
            user_id = request.user
            UserInfo.objects.filter(id=user_id).update(
                last_login_time=datetime.datetime.now().replace(microsecond=0)
            )

        return response
