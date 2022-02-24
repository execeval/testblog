from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from rest_flex_fields import FlexFieldsModelSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer


import core.models

Account = get_user_model()


class CurrentUserUsernameDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.username

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ImageSerializer(VersatileImageFieldSerializer):
    def __init__(self, *args, **kwargs):
        sizes = [
            ('full_size', 'url'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__200x200')
        ]
        super().__init__(sizes, *args, **kwargs)


class GetAccountByNameSerializer(serializers.Serializer):
    account = serializers.SlugRelatedField(slug_field='username', queryset=Account.objects.all(), required=True
                                           , allow_null=False)


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'date_joined', 'last_login', 'name']
        read_only_fields = fields


class PublicAccountSerializer(FlexFieldsModelSerializer):
    """Сериалайзер с полями, которые может просматривать любой пользователь сайта"""

    id = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

    class Meta:
        model = Account
        fields = ['id', 'username', 'profile_picture', 'date_joined', 'last_login', 'is_admin',  'is_staff']
        expandable_fields = {'profile_picture': ImageSerializer}


class MakePostSerializer(FlexFieldsModelSerializer):
    """Сериалайзер для публикации постов"""
    categories = serializers.PrimaryKeyRelatedField(queryset=core.models.Post.objects.all(), many=True)

    class Meta:
        model = core.models.Post
        fields = ['title', 'content', 'date', 'active', 'categories']

    def _get_author(self):
        return self.context.get('request').user

    def create(self, validated_data):
        validated_data['author'] = self._get_author()
        return super().create(validated_data)


class PostCategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = core.models.PostCategory
        fields = '__all__'


class PostSerializer(FlexFieldsModelSerializer):
    """Сериалайзер для чтения постов"""
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    categories = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = core.models.Post
        fields = ['id', 'author', 'title', 'content', 'date', 'active', 'categories']
        expandable_fields = {'author': PublicAccountSerializer,
                             'categories': (PostCategorySerializer, {'many': True})
                             }


class LimitOffsetSerializer(serializers.Serializer):
    limit = serializers.IntegerField(min_value=1, required=False)
    offset = serializers.IntegerField(min_value=0, required=False)


class PrivateAccountSerializer(FlexFieldsModelSerializer):
    """Сериалайзер с полями, которые может просматривать только владелец аккаунта или staff"""

    id = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

    class Meta:
        model = Account
        fields = ['id', 'username', 'profile_picture', 'date_joined', 'last_login', 'is_admin',  'is_staff',
                  'email', 'is_active']
        expandable_fields = {'profile_picture': ImageSerializer}


class CreateAccountByOwnerSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_password(self, value):
        validate_password(value)
        return make_password(value)

    class Meta:
        model = Account
        fields = ['id', 'username', 'profile_picture', 'image_ppoi', 'email', 'is_staff', 'password',
                  'is_active']
        expandable_fields = {'profile_picture': ImageSerializer}


class ReactionSerializer(FlexFieldsModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = core.models.PostReaction
        fields = '__all__'
        expandable_fields = {
            'post': PostSerializer,
            'author': PublicAccountSerializer}


class CommentSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = core.models.PostComment
        fields = '__all__'
        extra_kwargs = {'author': {'read_only': True}}
        expandable_fields = {
            'post': PostSerializer,
            'author': PublicAccountSerializer}


class ReactionChangeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = core.models.PostReaction
        fields = '__all__'
        extra_kwargs = {'author': {'read_only': True},
                        'post': {'read_only': True}}


class CommentChangeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = core.models.PostComment
        fields = '__all__'
        extra_kwargs = {'author': {'read_only': True},
                        'post': {'read_only': True}}


class CreateAccountSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_password(self, value):
        validate_password(value)
        return make_password(value)

    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'profile_picture', 'image_ppoi', 'password']
        expandable_fields = {
            'profile_picture': ImageSerializer}


class CreateAccountPrivilegedSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_password(self, value):
        validate_password(value)
        return make_password(value)

    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'profile_picture', 'image_ppoi', 'password', 'is_staff', 'is_active']
        expandable_fields = {
            'profile_picture': ImageSerializer}


class ReadAccountSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'profile_picture', 'image_ppoi',
                  'date_joined', 'last_login', 'is_admin', 'is_staff']
        expandable_fields = {'profile_picture': ImageSerializer}


class ReadAccountPrivilegedSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'profile_picture', 'image_ppoi',
                  'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active']
        expandable_fields = {'profile_picture': ImageSerializer}


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)