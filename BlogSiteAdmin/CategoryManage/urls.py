from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^category/list", QueryCategoryView.as_view()),
    url(r"^category/add", AddCategoryView.as_view()),
    url(r"^category/edit", EditCategoryView.as_view()),
    url(r"^category/delete", DeleteCategoryView.as_view()),
]