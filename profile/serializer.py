from drf_yasg.utils import logger
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from .models import Profile


class CreateProfileSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    profile_name = serializers.CharField(required=True)
    pin_num = serializers.IntegerField(required=True)

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

            profile = Profile.objects.create(
                user_id=validated_data['user_id'],
                email=validated_data['email']
            )
            return profile
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")  # Log any errors during creation
            raise APIException(detail="Error creating profile.",
                               code=status.HTTP_500_INTERNAL_SERVER_ERROR)