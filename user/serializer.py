import bcrypt

from drf_yasg.utils import logger
from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password_check = serializers.CharField(write_only=True)
    email = serializers.CharField()
    certifi_num = serializers.IntegerField()

    def validate_user_id(self, value):
        """
        Check if the user_id already exists.
        """
        if User.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("This user_id is already taken.")
        return value

    def validate(self, data):
        """
        Ensure that the two password fields match.
        """
        if data['password'] != data['password_check']:
            raise serializers.ValidationError("Passwords do not match.")
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
            raise serializers.ValidationError("Error creating user.")


class CheckPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    check_password = serializers.CharField()
