from django.conf.urls import url, include
from django.urls import re_path, path
from django.views.generic.base import TemplateView
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    url('^admin/', include("UserManage.urls")),
    url('^admin/', include("CategoryManage.urls")),
    url('^admin/', include("TagManage.urls")),
    url('^admin/', include("ArticleManage.urls")),
    url('^admin/', include("CommonManage.urls")),
    url('^q/', include("QueryManage.urls")),
    path('', TemplateView.as_view(template_name="../frontend/index.html")),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
