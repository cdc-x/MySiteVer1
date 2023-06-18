import logging
import datetime
import traceback
import markdown
from lxml import etree
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from CategoryManage.models import Category
from TagManage.models import Tag
from .serializers import *

logger = logging.getLogger("log")


class QueryCategoryMapView(APIView):
    @staticmethod
    def get(request):
        try:
            category_list = list()
            tag_list = list()

            category_query = Category.objects.all().order_by("category")
            for item in category_query:
                category_list.append({"label": item.category, "value": item.id})

            tag_query = Tag.objects.all().order_by("tag")
            for item in tag_query:
                tag_list.append({"label": item.tag, "value": item.id})

            ret_data = {"status_code": 1000, "category": category_list, "tag": tag_list}
            logger.info(
                f"【查询分类/标签映射】-【成功】- 分类数据量：{str(len(category_list))} - 标签数据量：{str(len(tag_list))}")
        except Exception as e:
            logger.error(f"【查询分类/标签映射】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class QueryArticleView(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data

            title = data.get("article", "")
            current_page = data.get("page", 1)
            page_size = data.get("pageSize", 10)

            queryset = Article.objects.filter(title__icontains=title).order_by("-publish_time", "-title")

            paginator = Paginator(list(queryset), page_size)
            try:
                page_content = paginator.page(current_page)
            except EmptyPage as e:
                logger.error(str(e))
                page_content = paginator.page(1)
                current_page = 1

            serializer = ArticleSerializer(page_content, many=True)

            ret_data = {"status_code": 1000, "data": serializer.data, "total": queryset.count(), "page_size": page_size,
                        "page": current_page}
            logger.info(f"【查询文章】-【成功】- 数据量：{str(queryset.count())}")
        except Exception as e:
            logger.error(f"【查询文章】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class AddArticleView(APIView):

    @staticmethod
    def create_desc(content):

        try:
            _html = etree.HTML(markdown.markdown(content))
            _content_list = _html.xpath("//p/text()")
            _content_list = [i.replace("\u200b", "").strip() for i in _content_list]

            _content = "".join(_content_list)
            desc = _content.strip()[:200]
        except Exception as e:
            logger.error(f"【新增文章】-【自动生成简介】-【失败】- {str(e)} - {traceback.format_exc()}")
            desc = ""

        return desc

    def post(self, request):
        try:
            data = request.data
            article_title = data.get("title", "")
            query = Article.objects.filter(title=article_title)
            category = data.get("category", "")
            tag_list = data.get("tag", [])
            main_tag = data.get("mainTag", "")
            desc = data.get("desc", "")
            content = data.get("content", "")

            self.create_desc(content)

            logger.info(f"【新增文章】-【{article_title}】-【{str(category)}】-【{str(tag_list)}】")

            if query:
                ret_data = {"status_code": 1001, "message": "已存在同名文章"}
                logger.error(f"【新增文章】-【{article_title}】-【失败】-【已存在同名文章】")
            else:

                # 编辑文章简介
                if not desc:
                    desc = self.create_desc(content)

                obj = Article.objects.create(
                    title=article_title,
                    article_desc=desc,
                    content=content,
                    publish_time=datetime.datetime.strptime(data.get("publish_time"), "%Y-%m-%d"),
                    category_id=category,
                )

                # 新增分类
                for tag_id in tag_list:
                    Article2Tag.objects.create(article_id=obj.id, tag_id=tag_id, main=0)

                # 设置主分类
                Article2Tag.objects.filter(article_id=obj.id, tag_id=main_tag).update(
                    main=1
                )
                ret_data = {"status_code": 1000, "message": "新增文章成功"}
                logger.info(f"【新增文章】-【{article_title}】-【成功】")
        except Exception as e:
            logger.info(f"【新增文章】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class EditArticleView(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            aid = data.get("aid", "")
            title = data.get("title", "")
            tag_list = data.get("tag", [])
            main_tag = data.get("mainTag", "")

            query = Article.objects.filter(Q(title=title) & ~Q(id=aid))

            if query:
                ret_data = {"status_code": 1001, "message": "已存在同名文章"}
                logger.error(f"【修改文章】-【{str(aid)}】-【失败】-【已存在同名文章】")
            else:
                obj = Article.objects.filter(id=aid).first()
                obj.title = title
                obj.article_desc = data.get("article_desc", "")
                obj.content = data.get("content", "")
                obj.category_id = data.get("category", "")
                obj.publish_time = datetime.datetime.strptime(data.get("publish_time"), "%Y-%m-%d")

                # 先清除原有的绑定关系
                Article2Tag.objects.filter(article_id=aid).delete()

                # 重新绑定关系
                for tag_id in tag_list:
                    Article2Tag.objects.create(article_id=obj.id, tag_id=tag_id, main=0)
                # 设置主标签
                Article2Tag.objects.filter(article_id=obj.id, tag_id=main_tag).update(
                    main=1
                )

                obj.save()
                ret_data = {"status_code": 1000, "message": "修改文章成功"}
                logger.info(f"【修改文章】-【{str(aid)}】-【成功】")

        except Exception as e:
            logger.error(f"【修改文章】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class DeleteArticleView(APIView):

    @staticmethod
    def get(request):
        try:
            aid = request.GET.get("id", "")
            obj = Article.objects.filter(id=aid).first()

            if not obj:
                ret_data = {"status_code": 1001, "message": "未找到文章信息"}
                logger.error(f"【删除文章】-【{str(aid)}】-【失败】-【未找到文章信息】")
            else:
                with transaction.atomic():
                    obj.delete()
                    ret_data = {"status_code": 1000, "message": "删除文章成功"}
                    logger.info(f"【删除文章】-【{str(aid)}】-【成功】")
        except Exception as e:
            logger.error(f"【删除文章】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)
