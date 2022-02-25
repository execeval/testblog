import core.models

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from core.serializers.account import AuthorExpandedSerializer
from core.serializers.post import PostExpandedSerializer


class ReactionSerializer(FlexFieldsModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = core.models.PostReaction
        fields = '__all__'
        expandable_fields = {
            'post': PostExpandedSerializer,
            'author': AuthorExpandedSerializer}


class ReactionChangeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = core.models.PostReaction
        fields = '__all__'
        extra_kwargs = {'author': {'read_only': True},
                        'post': {'read_only': True}}
        expandable_fields = {
            'post': PostExpandedSerializer,
            'author': AuthorExpandedSerializer}