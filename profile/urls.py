from django.urls import path

from .views import MemberAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'profile'

urlpatterns = [
    path('profile', MemberAPIView.as_view(), name='profile'),
]
