# urls.py
from django.urls import path
from .views import send_notification_view  # 알맞은 경로로 임포트

urlpatterns = [
    path('send-notification/', send_notification_view, name='send_notification'),
]