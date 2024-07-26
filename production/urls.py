from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.routers import DefaultRouter
from django.urls import path

# 모델 정의 (예시)
from .models import Product  # 실제 모델로 변경

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="LogicPuzzle API",
        default_version='v1',
        description="API documentation for LogicPuzzle project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('api/', include('your_app.urls')),  # 실제 앱 URL 설정으로 변경
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]