from django.urls import path

from auth.views import LoginAPIView
from .views import SignupAPIView, UserCheckAPIView, SendVerifyCode, CheckVerifyCode, LoginAPIView, CheckIdAPIView,ChpasswdAPIView

app_name = 'user'

urlpatterns = [
    path('signup', SignupAPIView.as_view(), name='signup'),
    path('checkId', UserCheckAPIView.as_view(), name='checkId'),
    path('send-verify-code', SendVerifyCode.as_view(), name='sendVerifyCode'),
    path('check-verify-code', CheckVerifyCode.as_view(), name='checkVerifyCode'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('check-id/', CheckIdAPIView.as_view(), name='check_id'),
    path('chpasswd/', ChpasswdAPIView.as_view(), name='chpasswd'),
]
