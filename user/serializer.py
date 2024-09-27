import json

from drf_yasg.utils import logger
from rest_framework import serializers
from .models import User


class CreateUserSerializer(serializers.Serializer):
    userId = serializers.CharField(source='user_id')
    password = serializers.CharField(write_only=True)
    email = serializers.CharField()

    def create(self, validated_data):
        """
        Create a new board instance and return it as a JSON object.
        """
        try:
            user = User.objects.create(
                user_id=validated_data['user_id'],
                password=validated_data['password'],
                email=validated_data['email']
            )
            logger.debug(f"User created with ID: {user.userId}")  # Log success
            return user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")  # Log any errors during creation
            raise serializers.ValidationError("Error creating user.")


class CheckPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    check_password = serializers.CharField()
