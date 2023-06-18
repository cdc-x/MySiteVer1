from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^tag/list", QueryTagView.as_view()),
    url(r"^tag/add", AddTagView.as_view()),
    url(r"^tag/edit", EditTagView.as_view()),
    url(r"^tag/delete", DeleteTagView.as_view()),
]