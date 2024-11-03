from django.urls import path

from .views import MemberAPIView

app_name = 'profile'

urlpatterns = [
    path('profile', MemberAPIView.as_view(), name='profile'),
]
