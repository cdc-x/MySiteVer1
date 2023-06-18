import traceback
import logging
import datetime
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

logger = logging.getLogger("log")


class QueryCategoryView(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            category = data.get("category", "")
            current_page = data.get("page", 1)
            page_size = data.get("pageSize", 10)

            queryset = Category.objects.filter(category__icontains=category).order_by("-create_time", "category")
            paginator = Paginator(queryset, page_size)
            try:
                page_content = paginator.page(current_page)
            except EmptyPage as e:
                logger.error(str(e))
                page_content = paginator.page(1)
                current_page = 1

            serializer = CategorySerializer(page_content, many=True)

            ret_data = {"status_code": 1000, "data": serializer.data, "total": queryset.count(), "page_size": page_size,
                        "page": current_page}
            logger.info(f"【查询分类】-【成功】- 数据条数：{str(queryset.count())}")
        except Exception as e:
            logger.error(f"【查询分类】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class AddCategoryView(APIView):

    @staticmethod
    def post(request):
        try:
            category = request.data.get("category", "")
            # 判断分类是否已经存在
            query = Category.objects.filter(category=category)
            if not query:
                category_info = dict()
                category_info["category"] = category
                category_info["create_time"] = datetime.datetime.now().replace(microsecond=0)

                serializer = CategorySerializer(data=category_info)

                if serializer.is_valid():
                    serializer.save()
                    ret_data = {"status_code": 1000, "message": "新增分类成功", "data": serializer.data}
                    logger.info(f"【新增分类】-【成功】- 【{category}】")
                else:
                    ret_data = {"status_code": 1001, "message": "新增分类失败", "data": serializer.errors}
                    logger.error(f"【新增分类】-【失败】- 【{category}】-【{str(serializer.errors)}】")
            else:
                ret_data = {"status_code": 1001, "message": "已存在同名分类"}
                logger.error(f"【新增分类】-【失败】- 【{category}】-【已存在同名分类】")
        except Exception as e:
            logger.error(f"【新增分类】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class EditCategoryView(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            cid = data.get("id", "")
            category = data.get("category", "")
            query = Category.objects.filter(Q(category=category) & ~Q(id=cid))

            if query:
                ret_data = {"status_code": 1001, "message": "已存在同名的分类"}
                logger.error(f"【修改分类】-【{str(cid)}】-【失败】-【已存在同名的分类】")
            else:
                Category.objects.filter(id=cid).update(
                    category=category,
                    update_time=datetime.datetime.now().replace(microsecond=0)
                )
                ret_data = {"status_code": 1000, "message": "修改分类成功"}
                logger.info(f"【修改分类】-【{str(cid)}】-【成功】")
        except Exception as e:
            logger.error(f"【修改分类】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class DeleteCategoryView(APIView):

    @staticmethod
    def get(request):
        try:
            cid = request.GET.get("id", "")
            obj = Category.objects.filter(id=cid).first()

            if not obj:
                ret_data = {"status_code": 1001, "message": "未找到分类信息"}
                logger.error(f"【删除分类】-【{str(cid)}】-【失败】-【未找到分类信息】")
            else:
                with transaction.atomic():
                    obj.delete()
                    ret_data = {"status_code": 1000, "message": "删除分类成功"}
                    logger.info(f"【删除分类】-【{str(cid)}】-【成功】")
        except Exception as e:
            logger.error(f"【删除分类】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)
