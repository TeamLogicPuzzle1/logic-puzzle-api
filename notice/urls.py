from django.urls import path
from . import views

urlpatterns = [
    path('notices', views.NoticeListCreate.as_view(), name='notice_list_create'),
    path('notices/<int:pk>', views.NoticeDetail.as_view(), name='notice_detail'),
]