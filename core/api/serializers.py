from rest_flex_fields import FlexFieldsModelSerializer
from core.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation

UserModel = get_user_model()


class APIRegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("username", "password", "email", "name")
        write_only_fields = fields
        extra_kwargs = {'username': {'required': True}, 'password': {'required': True}, 'email': {'required': True}}

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user