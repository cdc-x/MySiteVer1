from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="分类ID")
    category = models.CharField(max_length=220, verbose_name="分类名")
    create_time = models.DateTimeField(null=True, blank=True, verbose_name="创建时间")
    update_time = models.DateTimeField(null=True, blank=True, verbose_name="修改时间")

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "category"
        db_table = verbose_name_plural
