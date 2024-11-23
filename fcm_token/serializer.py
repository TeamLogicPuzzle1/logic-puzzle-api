# serializers.py

from rest_framework import serializers
from user.models import User
from profile.models import Profile
from fcm_token.model import FcmToken


class FcmTokenSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.user_id', read_only=True)
    profile_id = serializers.IntegerField(source='profile.id', read_only=True)
    device_number = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        model = FcmToken
        fields = ['user_id', 'profile_id', 'device_number', 'token']

    def create(self, validated_data):
        # FcmToken 객체 생성 시 사용할 로직
        user_data = validated_data.pop('user')
        profile_data = validated_data.pop('profile')
        user = User.objects.get(user_id=user_data['user_id'])
        profile = Profile.objects.get(id=profile_data['id'], user=user)

        fcm_token, created = FcmToken.objects.update_or_create(
            user=user,
            profile=profile,
            device_number=validated_data['device_number'],
            defaults={'token': validated_data['token']}
        )
        return fcm_token

    def update(self, instance, validated_data):
        # FcmToken 객체 갱신 시 사용할 로직
        instance.device_number = validated_data.get('device_number', instance.device_number)
        instance.token = validated_data.get('token', instance.token)
        instance.save()
        return instance