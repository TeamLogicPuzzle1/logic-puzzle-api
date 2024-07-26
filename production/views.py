from rest_framework import viewsets, filters
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  # 모든 상품 조회
    serializer_class = ProductSerializer  # 연결된 시리얼라이저 클래스
    filter_backends = [filters.OrderingFilter]  # 정렬 필터 사용
    ordering_fields = ['name', 'expiration_date', 'quantity']  # 정렬 가능 필드
    ordering = ['name']  # 기본 정렬 필드

    def create(self, request, *args, **kwargs):
        data = request.data
        # 이름과 유통기한 필수 확인
        if 'name' not in data or 'expiration_date' not in data:
            return Response({"detail": "Name and expiration_date are required."}, status=400)

        # 선택 필드 기본값 설정
        if 'ocr' not in data:
            data['ocr'] = None
        if 'barcode' not in data:
            data['barcode'] = None
        if 'category' not in data:
            data['category'] = None
        if 'location' not in data:
            data['location'] = None
        if 'quantity' not in data:
            data['quantity'] = None
        if 'memo' not in data:
            data['memo'] = None

        # 시리얼라이저로 데이터 검증 및 저장
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)