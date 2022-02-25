import core.models

from rest_flex_fields import FlexFieldsModelSerializer
from core.serializers.account import AuthorExpandedSerializer
from core.serializers.post import PostExpandedSerializer


class CommentSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = core.models.PostComment
        fields = '__all__'
        extra_kwargs = {'author': {'read_only': True}}
        expandable_fields = {
            'post': PostExpandedSerializer,
            'author': AuthorExpandedSerializer}


class CommentChangeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = core.models.PostComment
        fields = '__all__'
        extra_kwargs = {'author': {'read_only': True},
                        'post': {'read_only': True},
                        'id': {'read_only': True}}
        expandable_fields = {
            'post': PostExpandedSerializer,
            'author': AuthorExpandedSerializer}
