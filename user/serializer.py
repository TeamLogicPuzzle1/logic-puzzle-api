import json
from rest_framework import serializers
from .models import User


class CreateUserSerializer(serializers.Serializer):
    userId = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def create(self, validated_data):
        """
        Create a new board instance and return it as a JSON object.
        """
        user = User.objects.create(**validated_data)
        return json.dumps({
            "userId": user.userId,
            "password": user.password,
            "email": user.email
        })


class CheckPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    check_password = serializers.CharField()
