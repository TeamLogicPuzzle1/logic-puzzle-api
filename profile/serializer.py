from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import logger
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from .models import Profile


class CreateProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, write_only=True)
    profile_name = serializers.CharField(required=True)
    pin_num = serializers.IntegerField(required=True, write_only=True)
    leader_yn = serializers.CharField(read_only=True)
    member_id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        pin_str = str(data['pin_num'])
        if not pin_str.isdigit() or len(pin_str) != 6:
            raise serializers.ValidationError("PIN number must contain only digits.")
        return data

    def create(self, validated_data):
        """
        Create a new board instance and return it as a JSON object.
        """
        try:
            pin_code_str = str(validated_data['pin_num'])
            hashed_code = make_password(pin_code_str)

            is_existing_user = Profile.objects.filter(user_id=validated_data['id']).exists()

            # leader_yn 설정: user_id가 이미 존재하면 False, 그렇지 않으면 True
            leader_check = not is_existing_user

            profile = Profile.objects.create(
                user_id=validated_data['id'],
                profile_name=validated_data['profile_name'],
                pin_num = hashed_code,
                leader_yn=leader_check
            )
            return profile
        except Exception as e:
            logger.error(f"Error creating profile: {str(e)}")  # Log any errors during creation
            raise APIException(detail="Error creating profile.",
                               code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'