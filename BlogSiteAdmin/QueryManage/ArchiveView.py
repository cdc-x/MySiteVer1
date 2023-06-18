import traceback
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from ArticleManage.models import *

logger = logging.getLogger("log")


class ArticleArchiveView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            pub_info = dict()
            pub_list = list()
            article_query = Article.objects.all().order_by("publish_time")

            for _obj in article_query:
                if str(_obj.publish_time.strftime("%Y-%m-%d")) not in pub_info:
                    pub_info[str(_obj.publish_time.strftime("%Y-%m-%d"))] = list()

                category = _obj.category.category

                tags_list = list()
                tags_query = Article2Tag.objects.filter(article_id=_obj.id)
                for tag in tags_query:
                    tags_list.append(f"【{tag.tag}】")
                tag = "".join(tags_list)

                pub_info[str(_obj.publish_time.strftime("%Y-%m-%d"))].append(
                    {"id": _obj.id, "title": _obj.title, "category": category, "tag": tag}
                )

            for date in pub_info:
                pub_list.append(
                    {
                        "time": date,
                        "articles": pub_info[date]
                    }
                )

            pub_list.sort(key=lambda x: x["time"], reverse=True)

            ret_data = {"status_code": 1000, "data": pub_list}
        except Exception as e:
            ret_data = {"status_code": 1001, "message": str(e)}
            logger.error(f"【关于本站】-【失败】- {str(e)} - {traceback.format_exc()}")

        return Response(ret_data)
