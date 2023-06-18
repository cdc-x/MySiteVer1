from django.db import models


class UserInfo(models.Model):
    id = models.CharField(max_length=64, primary_key=True, verbose_name="用户ID")
    username = models.CharField(max_length=64, null=False, verbose_name="用户名")
    password = models.CharField(max_length=64, null=False, verbose_name="登录密码")
    last_login_time = models.DateTimeField(verbose_name="最近登录时间", null=True, blank=True)
    token = models.CharField(max_length=255, verbose_name="登录的token", null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "user_info"
        db_table = verbose_name_plural
