import core.models

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from core.serializers.account import AuthorExpandedSerializer

from core.serializers.category import PostCategorySerializer
from core.models import Post


class PostSerializer(FlexFieldsModelSerializer):
    """Сериалайзер для чтения постов"""
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=core.models.PostCategory.objects.all(), many=True)

    class Meta:
        model = core.models.Post
        fields = ['id', 'author', 'title', 'content', 'date', 'is_active', 'categories']
        expandable_fields = {'author': AuthorExpandedSerializer,
                             'categories': (PostCategorySerializer, {'many': True})
                             }


class PostExpandedSerializer(FlexFieldsModelSerializer):
    """Сериалайзер для чтения постов"""
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=core.models.PostCategory.objects.all(), many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if isinstance(instance, Post) and data.get('is_active') is False:
            data = {'id': data['id'], 'is_active': False}

        return data

    class Meta:
        model = core.models.Post
        fields = ['id', 'author', 'title', 'content', 'date', 'is_active', 'categories']
