import email
import threading

import bcrypt
from drf_yasg.utils import logger
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from .models import User


class CreateUserSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    id_check = serializers.BooleanField(default=False)
    password = serializers.CharField(write_only=True)
    password_check = serializers.CharField(write_only=True)
    email = serializers.CharField()
    verify_check = serializers.BooleanField(default=False)

    def validate(self, data):
        """
        Ensure that the two password fields match.
        """
        # Password match check
        if data['password'] != data['password_check']:
            raise serializers.ValidationError("Passwords do not match.")

        # Double check field validation (should be True)
        if not data.get('id_check', False):  # Ensures that it is explicitly True
            raise serializers.ValidationError("The id check option must be confirmed (True).")

        # Verify check field validation (should be True)
        if not data.get('verify_check', False):  # Ensures that it is explicitly True
            raise serializers.ValidationError("The verify check option must be confirmed (True).")

        return data

    def create(self, validated_data):
        """
        Create a new board instance and return it as a JSON object.
        """
        try:
            # Hash the password
            hashed_password = bcrypt.hashpw(validated_data['password'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            user = User.objects.create(
                user_id=validated_data['user_id'],
                password=hashed_password,
                email=validated_data['email']
            )
            logger.debug(f"User created with ID: {user.user_id}")   # Log success
            return user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")  # Log any errors during creation
            raise APIException(detail="Error creating user.",
                               code=status.HTTP_500_INTERNAL_SERVER_ERROR)