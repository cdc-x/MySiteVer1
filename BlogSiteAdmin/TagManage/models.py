from django.db import models


class Tag(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="标签ID")
    tag = models.CharField(max_length=220, verbose_name="标签名")
    create_time = models.DateTimeField(null=True, blank=True, verbose_name="创建时间")
    update_time = models.DateTimeField(null=True, blank=True, verbose_name="修改时间")

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name_plural = "tag"
        db_table = verbose_name_plural
