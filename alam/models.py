from django.db import models

class User(models.Model):
    # 유저 모델 정의 (예: 이름, 이메일, FCM 토큰 등)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    fcm_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username