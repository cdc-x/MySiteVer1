from django.conf.urls import url
from .DashboardView import QueryDashboardDataView
from .ArchiveView import ArticleArchiveView
from .ArticleViews import *

urlpatterns = [
    # ��ѯ�������ͳ������
    url(r"^about_site$", QueryDashboardDataView.as_view()),
    # ���¹鵵��Ϣ
    url(r"^archive$", ArticleArchiveView.as_view()),
    # ��ѯ�����б�
    url(r"^article/all$", QueryArticleListView.as_view()),
    # ��ѯ������������
    url(r"^article/hot$", QueryHotArticleListView.as_view()),
    # ��ѯTag����
    url(r"^article/tags$", QueryArticleTagsView.as_view()),
    # ��ѯ����
    url(r"^article/category$", QueryArticleCategoryView.as_view()),
    # ��ѯ��������
    url(r"^article/content$", QueryArticleContentView.as_view()),
    # ��ȡ���µ�����
    url(r"^article/count/thumb$", QueryArticleThumbView.as_view()),
    # ��ȡ�����Ķ���
    url(r"^article/count/browse$", QueryArticleBrowseView.as_view()),
    # ��鵱ǰ�û��Ƿ�����µ���
    url(r"^article/check/thumb$", CheckArticleThumbView.as_view()),
    # ���µ���
    url(r"^article/thumb$", ArticleThumbView.as_view()),
    # �������·����ѯ����
    url(r"^article/search_by_category$", SearchArticleByCategoryView.as_view()),
    # �������±�ǩ��ѯ����
    url(r"^article/search_by_tag$", SearchArticleByTagView.as_view()),

]
