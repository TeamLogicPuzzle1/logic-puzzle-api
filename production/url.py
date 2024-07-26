from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

# 라우터 설정
router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),  # 라우터 URL 포함
]