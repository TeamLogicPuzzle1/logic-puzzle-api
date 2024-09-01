from rest_framework import viewsets, filters
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'expiration_date', 'quantity']
    ordering = ['name']

    def create(self, request, *args, **kwargs):
        # 데이터 검증 및 처리 시 시리얼라이저를 사용
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 시리얼라이저의 validate 메소드를 호출하여 검증
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)