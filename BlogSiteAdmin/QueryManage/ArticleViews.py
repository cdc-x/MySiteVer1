import datetime
import logging
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import EmptyPage, Paginator
from ArticleManage.models import *
from TagManage.models import Tag
from CategoryManage.models import Category

logger = logging.getLogger("log")


class QueryArticleListView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            search_category = request.GET.get("category", "")
            search_tag = request.GET.get("tag", "")
            search_content = request.GET.get("content", "")
            page = request.GET.get("page", 1)

            if search_category:
                query = Article.objects.filter(category__category=search_category).order_by("-publish_time", "-title")
            elif search_tag:
                query = Article.objects.filter(
                    article2tag__tag__tag=search_tag, article2tag__main=True).order_by("-publish_time", "-title")
            elif search_content:
                query = Article.objects.filter(title__icontains=search_content).order_by("-publish_time", "-title")
            else:
                query = Article.objects.all().order_by("-publish_time", "-title")

            paginator = Paginator(query, 8)

            try:
                page_content = paginator.page(page)
            except EmptyPage as e:
                logger.error(str(e))
                page_content = []

            data_list = list()
            for obj in page_content:
                tags_list = list()
                tags_query = Article2Tag.objects.filter(article_id=obj.id)
                main_tag = Article2Tag.objects.filter(article_id=obj.id, main=True).first().tag.tag
                for tag in tags_query:
                    tags_list.append(tag.tag.tag)

                data_list.append({
                    "id": obj.id,
                    "title": obj.title,
                    "desc": obj.article_desc,
                    "publish_year": obj.publish_time.year,
                    "publish_month": obj.publish_time.month,
                    "publish_day": obj.publish_time.day,
                    "thumb": obj.thumb,
                    "browse": obj.browse,
                    "category": obj.category.category,
                    "tags": tags_list,
                    "main_tag": main_tag
                })

            ret_data = {"status_code": 1000, "data": data_list, "total": len(query), "page": page}
            logger.info(f"【查询文章列表】-【成功】- 文章数：{len(query)}")
        except Exception as e:
            logger.error(f"【查询文章列表】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class QueryHotArticleListView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            data_list = list(Article.objects.values("title", "id").order_by("-browse")[0:10])
            ret_data = {"status_code": 1000, "data": data_list}
            logger.info(f"【查询热门文章】-【成功】- 文章数：{len(data_list)}")
        except Exception as e:
            logger.error(f"【查询热门文章】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class QueryArticleTagsView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            tag_list = Tag.objects.values("id", "tag")
            ret_data = {"status_code": 1000, "data": tag_list}
            logger.info(f"【查询文章标签】-【成功】- 文章数：{len(tag_list)}")
        except Exception as e:
            logger.error(f"【查询文章标签】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class QueryArticleCategoryView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            category_list = Category.objects.values("id", "category")
            ret_data = {"status_code": 1000, "data": category_list}
            logger.info(f"【查询文章分类】-【成功】- 文章数：{len(category_list)}")
        except Exception as e:
            logger.error(f"【查询文章分类】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class QueryArticleContentView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            aid = request.GET.get("p", "")
            obj = Article.objects.filter(id=aid).first()
            content = ""
            category = ""
            pub_time = ""
            if obj:
                content = obj.content
                category = obj.category.category
                pub_time = obj.publish_time.strftime("%Y-%m-%d") if obj.publish_time else ""
                obj.browse += 1
                obj.save()

            ret_data = {"status_code": 1000, "data": content, "category": category, "pub_time": pub_time}
            logger.info(f"【查询文章内容】-【成功】")
        except Exception as e:
            logger.error(f"【查询文章内容】-【失败】-{str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "data": "", "category": "", "pub_time": ""}

        return Response(ret_data)


class QueryArticleThumbView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            aid = request.GET.get("p", "")
            obj = Article.objects.filter(id=aid).first()
            thumb = 0
            if obj:
                thumb = obj.thumb
            ret_data = {"status_code": 1000, "data": thumb}
            logger.info(f"【查询文章点赞数】-【成功】")
        except Exception as e:
            logger.error(f"【查询文章点赞数】-【失败】-{str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "data": 0}

        return Response(ret_data)


class QueryArticleBrowseView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            aid = request.GET.get("p", "")
            obj = Article.objects.filter(id=aid).first()
            browse = 0
            if obj:
                browse = obj.browse
            ret_data = {"status_code": 1000, "data": browse}
            logger.info(f"【查询文章浏览数】-【成功】")
        except Exception as e:
            logger.error(f"【查询文章浏览数】-【失败】-{str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "data": 0}

        return Response(ret_data)


class ArticleThumbView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            host = request.META.get("REMOTE_ADDR", "")
            aid = request.GET.get("p", "")

            # 查询用户是否已赞过该篇文章
            query = ThumbRecord.objects.filter(host=host, article_id=aid)
            if not query:
                # 记录点赞信息
                ThumbRecord.objects.create(
                    host=host,
                    article_id=aid,
                    thumb_time=datetime.datetime.now()
                )

                # 文章点赞数加1
                obj = Article.objects.filter(id=aid).first()
                if obj:
                    obj.thumb += 1
                    obj.save()

            ret_data = {"status_code": 1000, "message": "success"}
            logger.info(f"【文章点赞】-【成功】")
        except Exception as e:
            logger.error(f"【文章点赞】-【失败】-{str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class CheckArticleThumbView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            host = request.META.get("REMOTE_ADDR", "")
            aid = request.GET.get("p", "")

            # 查询用户是否已赞过该篇文章
            query = ThumbRecord.objects.filter(host=host, article_id=aid)
            if query:
                flag = True
            else:
                flag = False
            ret_data = {"status_code": 1000, "flag": flag}
            logger.info(f"【查询文章点赞状态】-【成功】")
        except Exception as e:
            logger.error(f"【查询文章点赞状态】-【失败】-{str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "flag": False}

        return Response(ret_data)


class SearchArticleByCategoryView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            cid = request.GET.get("cid", "")
            article_list = Article.objects.filter(category_id=cid).values("id", "title").order_by(
                "-publish_time", "-title")
            logger.info(f"【根据分类查询文章列表】-【成功】- 文章数：{len(article_list)}")
            ret_data = {"status_code": 1000, "data": article_list}
        except Exception as e:
            logger.error(f"【根据分类查询文章列表】-【失败】-{str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class SearchArticleByTagView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        try:
            tid = request.GET.get("tid", "")
            aid_list = list(set(Article2Tag.objects.filter(tag_id=tid).values_list("article_id", flat=True)))
            article_list = Article.objects.filter(id__in=aid_list).values("id", "title").order_by(
                "-publish_time", "-title")
            logger.info(f"【根据标签查询文章列表】-【成功】- 文章数：{len(article_list)}")
            ret_data = {"status_code": 1000, "data": article_list}
        except Exception as e:
            logger.error(f"【根据标签查询文章列表】-【失败】-{str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)
