from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.FoodWasteListCreate.as_view(), name='food_waste_list_create'),
    path('detail/<int:pk>/', views.FoodWasteDetail.as_view(), name='food_waste_detail'),
]