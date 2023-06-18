import datetime
import logging
import traceback
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

logger = logging.getLogger("log")


class QueryTagView(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            tag = data.get("tag", "")
            current_page = data.get("page", 1)
            page_size = data.get("pageSize", 10)

            queryset = Tag.objects.filter(tag__icontains=tag).order_by("-create_time", "tag")
            paginator = Paginator(list(queryset), page_size)
            try:
                page_content = paginator.page(current_page)
            except EmptyPage as e:
                logger.error(str(e))
                page_content = paginator.page(1)
                current_page = 1

            serializer = TagSerializer(page_content, many=True)

            ret_data = {"status_code": 1000, "data": serializer.data, "total": queryset.count(), "page_size": page_size,
                        "page": current_page}
            logger.info(f"【查询标签】-【成功】- 数据量：{str(queryset.count())}")
        except Exception as e:
            logger.error(f"【查询标签】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class AddTagView(APIView):

    @staticmethod
    def post(request):
        try:
            tag = request.data.get("tag", "")
            # 判断分类是否已经存在
            query = Tag.objects.filter(tag=tag)
            if not query:
                tag_info = dict()
                tag_info["tag"] = tag
                tag_info["create_time"] = datetime.datetime.now().replace(microsecond=0)

                serializer = TagSerializer(data=tag_info)

                if serializer.is_valid():
                    serializer.save()
                    ret_data = {"status_code": 1000, "message": "新增标签成功", "data": serializer.data}
                    logger.info(f"【新增标签】-【{tag}】-【成功】")
                else:
                    ret_data = {"status_code": 1001, "message": "新增标签失败", "data": serializer.errors}
                    logger.error(f"【新增标签】-【{tag}】-【失败】- {str(serializer.errors)}")
            else:
                ret_data = {"status_code": 1001, "message": "已存在同名标签"}
                logger.error(f"【新增标签】-【{tag}】-【失败】-【已存在同名标签】")
        except Exception as e:
            logger.error(f"【新增标签】-【失败】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class EditTagView(APIView):

    @staticmethod
    def post(request):
        try:
            data = request.data
            tid = data.get("id", "")
            tag = data.get("tag", "")
            query = Tag.objects.filter(Q(tag=tag) & ~Q(id=tid))

            if query:
                ret_data = {"status_code": 1001, "message": "已存在同名的标签"}
                logger.error(f"【新增标签】-【{tid}】-【失败】-【已存在同名的标签】")
            else:
                Tag.objects.filter(id=tid).update(
                    tag=tag,
                    update_time=datetime.datetime.now().replace(microsecond=0)
                )
                ret_data = {"status_code": 1000, "message": "修改标签成功"}
                logger.info(f"【新增标签】-【{tid}】-【成功】")
        except Exception as e:
            logger.error(f"【新增标签】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)


class DeleteTagView(APIView):

    @staticmethod
    def get(request):
        try:
            tid = request.GET.get("id", "")
            obj = Tag.objects.filter(id=tid).first()

            if not obj:
                ret_data = {"status_code": 1001, "message": "未找到标签信息"}
                logger.error(f"【删除标签】-【{tid}】-【失败】-【未找到标签信息】")
            else:
                with transaction.atomic():
                    obj.delete()
                    ret_data = {"status_code": 1000, "message": "删除标签成功"}
                    logger.error(f"【删除标签】-【{tid}】-【成功】")
        except Exception as e:
            logger.error(f"【删除标签】- {str(e)} - {traceback.format_exc()}")
            ret_data = {"status_code": 1001, "message": str(e)}

        return Response(ret_data)
