from django.urls import path

from .views import MemberAPIView, LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'profile'

urlpatterns = [
    path('profile', MemberAPIView.as_view(), name='profile'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
]
