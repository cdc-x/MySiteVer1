import logging
import traceback
import datetime
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from ArticleManage.models import Article, Article2Tag
from .models import Browse

logger = logging.getLogger("log")


class DashboardView(APIView):
    @staticmethod
    def get(request):
        try:
            # 查询文章相关信息
            article_query = Article.objects.values("title", "browse", "thumb")
            article_list = list(article_query)
            article_list.sort(key=lambda x: x["browse"], reverse=True)

            # 总阅读量
            read_num = 0
            # 总点赞数
            thumb_num = 0
            # 阅读排行文章标题列表
            article_title_list = list()
            # 阅读排行文章阅读量列表
            article_browse_list = list()
            # 文章总数
            article_num = article_query.count()

            for _article in article_list:
                read_num += _article["browse"]
                thumb_num += _article["thumb"]

            for _article in article_list[0:20]:
                article_title_list.append(_article["title"])
                article_browse_list.append(_article["browse"])

            today = datetime.datetime.now()
            start = today - datetime.timedelta(days=30)
            # 访问量相关数据
            browse_query = Browse.objects.filter(browse_time__gte=start)
            # 总访问量
            browse_num = browse_query.count()
            # 日访问量
            date_info = list(
                Browse.objects.filter(browse_time__gte=start).values_list("browse_time", flat=True))
            date_list = list(set([i.strftime("%Y-%m-%d") for i in date_info]))
            date_list.sort()

            # 日访问量列表
            daily_browse_list = list()
            # 日用户量列表
            daily_user_list = list()
            for date in date_list:
                _daily_browse_num = Browse.objects.filter(browse_time__date=date).count()
                _daily_user_num = Browse.objects.filter(browse_time__date=date).values("host").distinct().count()
                daily_browse_list.append(_daily_browse_num)
                daily_user_list.append(_daily_user_num)

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

            # 标签分类
            tag_list = list()
            tag_info = Article2Tag.objects.all().values("tag__tag").annotate(Count("id"))
            for item in tag_info:
                tag_list.append(
                    {
                        "name": item["tag__tag"],
                        "value": item["id__count"]
                    }
                )

            ret_data = {
                "status_code": 1000,
                "data": {
                    "article_num": article_num,
                    "read_num": read_num,
                    "thumb_num": thumb_num,
                    "article_title_list": article_title_list,
                    "article_browse_list": article_browse_list,
                    "browse_num": browse_num,
                    "date_list": date_list,
                    "daily_browse_list": daily_browse_list,
                    "daily_user_list": daily_user_list,
                    "category_list": category_list,
                    "tag_list": tag_list
                }
            }
        except Exception as e:
            logger.error(f"{str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)
