from django.urls import path

from .views import SignupAPIView, UserCheckAPIView

app_name = 'user'

urlpatterns = [
    path('signup', SignupAPIView.as_view(), name='signup'),
    path('check', UserCheckAPIView.as_view(), name='check')
]
