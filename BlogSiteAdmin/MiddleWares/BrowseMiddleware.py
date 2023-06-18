import datetime
from django.utils.deprecation import MiddlewareMixin
from CommonManage.models import Browse
from ArticleManage.models import Article


class SiteBrowseMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        visit_path = request.path

        if not visit_path.__contains__("admin"):
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META.get("HTTP_X_FORWARDED_FOR")
            else:
                ip = request.META.get("REMOTE_ADDR")

            if ip:
                Browse.objects.create(
                    host=ip,
                    browse_time=datetime.datetime.now().replace(microsecond=0)
                )
