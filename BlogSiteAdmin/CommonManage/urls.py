from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^dashboard", DashboardView.as_view()),
]
