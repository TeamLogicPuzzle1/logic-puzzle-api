from django.urls import path

from .views import MemberAPIView, MemberListAPIView

app_name = 'profile'

urlpatterns = [
    path('profile', MemberAPIView.as_view(), name='profile'),
    path('profiles', MemberListAPIView.as_view(), name='profiles'),
]
