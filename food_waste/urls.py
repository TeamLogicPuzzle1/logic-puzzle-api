from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodWasteViewSet  # 올바른 경로로 임포트

router = DefaultRouter()
router.register(r'food-waste', FoodWasteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]