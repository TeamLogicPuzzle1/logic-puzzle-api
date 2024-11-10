from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    member_id = serializers.IntegerField(required=True, write_only=True)
    pin_num = serializers.IntegerField(required=True, write_only=True)