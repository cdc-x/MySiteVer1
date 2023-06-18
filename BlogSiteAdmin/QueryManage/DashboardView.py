import traceback
import logging
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from ArticleManage.models import *
from CommonManage.models import Browse

logger = logging.getLogger("log")


class QueryDashboardDataView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            # 访问量相关数据
            browse_query = Browse.objects.all()
            # 总访问量
            browse_num = browse_query.count()

            # 文章相关数据
            # 总阅读量
            read_num = 0
            # 总点赞数
            thumb_num = 0
            article_query = Article.objects.values("browse", "thumb")
            article_list = list(article_query)
            # 文章总数
            article_num = article_query.count()
            for _article in article_list:
                read_num += _article["browse"]
                thumb_num += _article["thumb"]

            # 统计文章发布数据
            publish_info = dict()
            publish_query = Article.objects.all().values("publish_time__date").annotate(Count("id"))
            for item in publish_query:
                if item["publish_time__date"].strftime("%Y-%m") not in publish_info:
                    publish_info[item["publish_time__date"].strftime("%Y-%m")] = 0

                publish_info[item["publish_time__date"].strftime("%Y-%m")] += item["id__count"]

            publish_date_list = list(publish_info.keys())
            publish_date_list.sort()

            publish_num_list = list()
            for date in publish_date_list:
                publish_num_list.append(publish_info[date])

            # 文章分类数
            category_list = list()
            category_info = Article.objects.all().values("category__category").annotate(Count("id"))
            for item in category_info:
                category_list.append(
                    {
                        "name": item["category__category"],
                        "value": item["id__count"]
                    }
                )

            ret_data = {
                "status_code": 1000,
                "data": {
                    "article_num": article_num,
                    "read_num": read_num,
                    "thumb_num": thumb_num,
                    "browse_num": browse_num,
                    "publish_date_list": publish_date_list,
                    "publish_num_list": publish_num_list,
                    "category_list": category_list
                }
            }
        except Exception as e:
            ret_data = {"status_code": 1001, "message": str(e)}
            logger.error(f"【关于本站】-【失败】- {str(e)} - {traceback.format_exc()}")

        return Response(ret_data)
