<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.FoodWasteListCreate.as_view(), name='food_waste_list_create'),
    path('detail/<int:pk>/', views.FoodWasteDetail.as_view(), name='food_waste_detail'),
]
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodWasteViewSet

router = DefaultRouter()
router.register(r'food_waste', FoodWasteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
>>>>>>> b1a42273d14747a7e473f1904d1d7b508364f847
