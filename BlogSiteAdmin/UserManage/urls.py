from django.conf.urls import url
from .views import *

urlpatterns = [
    # 用户登录
    url('^user/login$', UserLoginView.as_view()),
    # 用户退出
    url('^user/logout$', UserLogoutView.as_view()),
    # 新增用户
    url('^user/add$', AddUserView.as_view()),
]
