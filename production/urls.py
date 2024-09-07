from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
<<<<<<< HEAD
    path('', include(router.urls)),
=======
    path('', include(router.urls)),  # Router URLs 포함
>>>>>>> b1a42273d14747a7e473f1904d1d7b508364f847
]