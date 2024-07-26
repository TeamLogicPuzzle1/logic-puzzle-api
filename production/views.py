from django.shortcuts import render

# Create your views here.
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

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def custom_endpoint(self, request):
        # 사용자 정의 엔드포인트 예시
        return Response({'message': 'Custom endpoint response'})

# URL 라우터 설정
router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = router.urls