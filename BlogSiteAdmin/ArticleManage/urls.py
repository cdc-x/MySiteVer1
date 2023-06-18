from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^article/map", QueryCategoryMapView.as_view()),
    url(r"^article/list$", QueryArticleView.as_view()),
    url(r"^article/add$", AddArticleView.as_view()),
    url(r"^article/edit$", EditArticleView.as_view()),
    url(r"^article/delete$", DeleteArticleView.as_view()),
]