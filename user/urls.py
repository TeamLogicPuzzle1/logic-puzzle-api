from django.urls import path

from .views import SignupAPIView, UserCheckAPIView, SendVerifyCode, CheckVerifyCode

app_name = 'user'

urlpatterns = [
    path('signup', SignupAPIView.as_view(), name='signup'),
    path('check', UserCheckAPIView.as_view(), name='check'),
    path('sendVerifyCode', SendVerifyCode.as_view(), name='sendVerifyCode'),
    path('checkVerifyCode', CheckVerifyCode.as_view(), name='checkVerifyCode')
]
