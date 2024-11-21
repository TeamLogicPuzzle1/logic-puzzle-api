from django.urls import path

from .views import LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'auth'

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
]
