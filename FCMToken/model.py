from django.db import models
from .models import user, profile

class FCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fcm_tokens', to_field='user_id')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='fcm_tokens', to_field='id')
    device_number = models.CharField(max_length=100)  # 기기 식별자
    token = models.CharField(max_length=255)  # FCM 토큰
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 일시
    updated_at = models.DateTimeField(auto_now=True)  # 갱신 일시

    def __str__(self):
        return f"FCM Token for User {self.user.user_id} - Profile {self.profile.profile_id} - Device {self.device_number}"