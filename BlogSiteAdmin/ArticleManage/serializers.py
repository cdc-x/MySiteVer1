from rest_framework import serializers
from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    publish_time = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    tags_name = serializers.SerializerMethodField(read_only=True)
    tag = serializers.SerializerMethodField(read_only=True)
    main_tag = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_publish_time(obj):
        if not obj.publish_time:
            return ""

        return obj.publish_time.strftime("%Y-%m-%d")

    @staticmethod
    def get_category_name(obj):
        category = obj.category
        if category:
            return category.category
        else:
            return ""

    @staticmethod
    def get_tags_name(obj):
        tag_list = []
        tag_query = Article2Tag.objects.filter(article_id=obj.id)
        for tag_obj in tag_query:
            tag_list.append(tag_obj.tag.tag)

        return ";".join(tag_list)

    @staticmethod
    def get_tag(obj):
        tag = Article2Tag.objects.filter(article_id=obj.id).values_list("tag_id", flat=True)
        return list(tag)

    @staticmethod
    def get_main_tag(obj):
        main_tag_obj = Article2Tag.objects.filter(article_id=obj.id, main=True).first()

        return main_tag_obj.tag.id

    class Meta:
        model = Article
        fields = "__all__"
