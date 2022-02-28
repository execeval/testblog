from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_flex_fields import FlexFieldsModelSerializer

from account.models import Account
from rest_framework import serializers


class AuthorExpandedSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if isinstance(instance, Account) and data.get('is_active') is False:
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
        fields = ['id', 'email', 'username', 'password', 'is_active']


class CreateAccountPrivilegedSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_password(self, value):
        validate_password(value)
        return make_password(value)

    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'password', 'is_staff', 'is_active']


class ReadAccountSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username',
                  'date_joined', 'last_login', 'is_admin', 'is_staff']


class ReadAccountPrivilegedSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'username',
                  'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
