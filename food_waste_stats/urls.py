from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodWasteViewSet

router = DefaultRouter()
router.register(r'food_waste', FoodWasteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
