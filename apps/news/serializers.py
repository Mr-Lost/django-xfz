from rest_framework import serializers
from .models import News, NewsCategory, Comments, Banner
from apps.xfz_auth.serializers import UserSerializer


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id', 'name')


class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializer()

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail', 'pub_time', 'category', 'author')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comments
        fields = ('id', 'content', 'author', 'pub_time')


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ('id', 'image_url', 'link_to', 'priority')
