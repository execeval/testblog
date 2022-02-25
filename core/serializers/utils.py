from rest_framework import serializers


class IsActiveSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True, allow_null=False)


class LimitOffsetSerializer(serializers.Serializer):
    limit = serializers.IntegerField(min_value=1, required=False)
    offset = serializers.IntegerField(min_value=0, required=False)
