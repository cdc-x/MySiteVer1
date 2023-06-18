from django.db import models


class Article(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="文章ID")
    title = models.CharField(max_length=220, verbose_name="文章标题")
    article_desc = models.CharField(max_length=220, verbose_name="文章简介", null=True, blank=True)
    content = models.TextField(verbose_name="文章内容", null=True, blank=True)
    publish_time = models.DateTimeField(verbose_name="发布时间", null=True, blank=True)
    thumb = models.IntegerField(verbose_name="点赞数", default=0)
    browse = models.IntegerField(verbose_name="浏览数", default=0)
    # 文章表与分类表多对一
    category = models.ForeignKey(to="CategoryManage.Category", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "article"
        db_table = verbose_name_plural


# 文章和标签表
# 文章表与标签表多对多
class Article2Tag(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="记录ID")
    article = models.ForeignKey(to="ArticleManage.Article", on_delete=models.CASCADE, verbose_name="文章ID")
    tag = models.ForeignKey(to="TagManage.Tag", on_delete=models.CASCADE, verbose_name="标签ID")
    main = models.BooleanField(verbose_name="是否为主要的标签")

    def __str__(self):
        return f"{self.article_id}_{self.tag_id}"

    class Meta:
        verbose_name_plural = "article_2_tag"
        db_table = verbose_name_plural


# 点赞记录表
class ThumbRecord(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="点赞记录ID")
    host = models.CharField(max_length=32, verbose_name="点赞的用户")
    article_id = models.CharField(max_length=64, verbose_name="文章ID")
    thumb_time = models.DateTimeField(verbose_name="点赞时间")

    def __str__(self):
        return self.host

    class Meta:
        verbose_name_plural = "thumb_record"
        db_table = verbose_name_plural
