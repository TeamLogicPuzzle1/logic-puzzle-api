from django.urls import path

from .views import SignupAPIView, UserCheckAPIView, SendVerificationCode

app_name = 'user'

urlpatterns = [
    path('signup', SignupAPIView.as_view(), name='signup'),
    path('check', UserCheckAPIView.as_view(), name='check'),
    path('sendVerifyCode', SendVerificationCode.as_view(), name='sendVerifyCode')
]
