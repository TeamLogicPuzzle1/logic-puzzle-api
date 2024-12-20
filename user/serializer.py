import email
import threading

import bcrypt
from drf_yasg.utils import logger
from rest_framework import serializers, status
from rest_framework.exceptions import APIException
import re
from .models import User


class CreateUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.CharField()
    id_check = serializers.BooleanField(default=False, write_only=True)
    password = serializers.CharField(write_only=True)
    password_check = serializers.CharField(write_only=True)
    email = serializers.CharField()
    verify_check = serializers.BooleanField(default=False, write_only=True)

    def validate(self, data):
        """
        Ensure that the two password fields match.
        """
        # Password match check
        if data['password'] != data['password_check']:
            raise serializers.ValidationError("Passwords do not match.")

        # Double check field validation (should be True)
        if not data.get('id_check', True):  # Ensures that it is explicitly True
            raise serializers.ValidationError("The id check option must be confirmed (True).")

        # Verify check field validation (should be True)
        if not data.get('verify_check', True):  # Ensures that it is explicitly True
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

class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        ref_name = "UserLoginSerializer"
    def validate(self, data):
        user_id = data.get('user_id')
        password = data.get('password')

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User ID not found.")

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise serializers.ValidationError("Invalid password.")

        return {"user_id": user.user_id}

class CheckIdSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    is_verified = serializers.BooleanField(required=True)

    def validate_email(self, value):
        # 이메일이 비어 있는지 여부만 확인
        if not value.strip():
            raise serializers.ValidationError("유효한 이메일 주소를 입력해 주세요.")
        return value