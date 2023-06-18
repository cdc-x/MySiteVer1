from django.db import models


class Browse(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="访问数据ID")
    host = models.CharField(max_length=32, verbose_name="访问的IP")
    browse_time = models.DateTimeField(verbose_name="访问时间")

    def __str__(self):
        return self.host

    class Meta:
        verbose_name_plural = "browse"
        db_table = verbose_name_plural
