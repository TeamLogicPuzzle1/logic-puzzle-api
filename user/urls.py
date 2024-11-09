from django.urls import path

from .views import SignupAPIView, UserCheckAPIView, SendVerifyCode, CheckVerifyCode

app_name = 'user'

urlpatterns = [
    path('signup', SignupAPIView.as_view(), name='signup'),
    path('checkId', UserCheckAPIView.as_view(), name='checkId'),
    path('send-verify-code', SendVerifyCode.as_view(), name='sendVerifyCode'),
    path('check-verify-code', CheckVerifyCode.as_view(), name='checkVerifyCode')
]
