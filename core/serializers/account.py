from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_flex_fields import FlexFieldsModelSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer

from account.models import Account
from rest_framework import serializers


class ImageSerializer(VersatileImageFieldSerializer):
    def __init__(self, *args, **kwargs):
        sizes = [
            ('full_size', 'url'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__200x200')
        ]
        super().__init__(sizes, *args, **kwargs)


class AuthorExpandedSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'profile_picture', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active']
        expandable_fields = {'profile_picture': ImageSerializer}

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if not data['is_active']:
            data = {'id': data['id'], 'is_active': False}

        return data


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
