"""
URL configuration for logicPuzzle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
<<<<<<< HEAD
from django.contrib import admin
=======
# from django.contrib import admin
>>>>>>> b1a42273d14747a7e473f1904d1d7b508364f847
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="LogicPuzzle API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls),
    path('api/production/', include('production.urls')),
    path('api/food_waste/', include('food_waste.urls')),
=======
    path('api/v1/user/', include('user.urls', namespace='user')),
    path('api/v1/foodWaste/', include('food_waste.urls')),
    path('api/v1/production/', include('production.urls')),
    path('api/v1/notice/', include('notice.urls')),
>>>>>>> b1a42273d14747a7e473f1904d1d7b508364f847
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
