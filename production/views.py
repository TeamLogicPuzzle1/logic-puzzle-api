import logging

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from user.models import User
from .models import Product
from .serializers import ProductCreateSerializer
from .servicelayer import extract_and_parse_expiration_date

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    lookup_field = 'product_id'

    # Swagger 파라미터 정의
    user_id_param = openapi.Parameter(
        'user_id', openapi.IN_QUERY, description="Filter products by user ID", type=openapi.TYPE_STRING, required=True
    )
    name_param = openapi.Parameter(
        'name', openapi.IN_QUERY, description="Filter products by name", type=openapi.TYPE_STRING
    )
    category_param = openapi.Parameter(
        'category', openapi.IN_QUERY, description="Filter products by category", type=openapi.TYPE_INTEGER
    )
    location_param = openapi.Parameter(
        'location', openapi.IN_QUERY, description="Filter products by location", type=openapi.TYPE_INTEGER
    )

    def get_queryset(self):
        """
        `user_id`는 필수, 추가로 name, category, location 필터링 적용
        """
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            logger.warning("user_id is missing in the request.")
            return Product.objects.none()  # user_id가 없는 경우 빈 쿼리셋 반환

        queryset = Product.objects.filter(user__user_id=user_id)

        # 동적 필터링
        name = self.request.query_params.get('name')
        category = self.request.query_params.get('category')
        location = self.request.query_params.get('location')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category=category)
        if location:
            queryset = queryset.filter(location=location)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[user_id_param, name_param, category_param, location_param],
        operation_description="List all products filtered by optional parameters and user_id.",
        responses={200: ProductCreateSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        필터링된 제품 목록 반환
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['post'], url_path='create-with-image', url_name='create_with_image')
    @swagger_auto_schema(
        operation_description="Create a product with an optional image file using user_id. If an image is provided, it attempts to extract the expiration date.",
        request_body=ProductCreateSerializer,
        responses={201: ProductCreateSerializer, 400: "Bad Request"},
    )
    @action(detail=False, methods=['post'], url_path='create-with-image', url_name='create_with_image')
    @swagger_auto_schema(
        operation_description="Create a product with an optional image file using user_id. If an image is provided, it attempts to extract the expiration date.",
        request_body=ProductCreateSerializer,
        responses={201: ProductCreateSerializer, 400: "Bad Request"},
    )
    def create_with_image(self, request):
        """
        이미지와 함께 제품 생성
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()  # user 처리 제거

            # 이미지 처리
            image = request.FILES.get('image')
            if image:
                logger.info(f"Received image file: {image.name}, size: {image.size}")
                try:
                    expiration_date = extract_and_parse_expiration_date(image)
                    if expiration_date:
                        product.expiration_date = expiration_date
                        product.save(update_fields=['expiration_date'])
                    else:
                        logger.warning("No expiration date could be extracted from the image.")
                except Exception as e:
                    logger.exception(f"Error processing image: {str(e)}")
                    return Response({"error": str(e)}, status=400)

            return Response(self.get_serializer(product).data, status=201)

        logger.error(f"Validation failed with errors: {serializer.errors}")
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        manual_parameters=[user_id_param],
        operation_description="Delete a product by product_id using user_id.",
        responses={
            204: "Product deleted successfully.",
            404: "Product not found.",
            403: "Forbidden: The product does not belong to the user_id."
        },
    )
    def destroy(self, request, *args, **kwargs):
        """
        user_id를 검증하여 제품 삭제
        """
        product_id = kwargs.get(self.lookup_field)
        user_id = request.query_params.get("user_id")

        if not user_id:
            logger.error("user_id is missing in the DELETE request.")
            return Response({"error": "user_id parameter is required."}, status=400)

        product = get_object_or_404(Product, product_id=product_id, user__user_id=user_id)

        product.delete()
        logger.info(f"Product {product_id} deleted successfully by user {user_id}.")
        return Response({"message": "Product deleted successfully."}, status=204)

    def update(self, request, *args, **kwargs):
        """
        Update a product by product_id using user_id
        """
        product_id = kwargs.get(self.lookup_field)
        logger.info(f"PUT request received for product_id: {product_id} by user_id: {request.data.get('user_id')}")

        # 요청 데이터에서 user_id 가져오기
        user_id = request.data.get('user_id')
        if not user_id:
            logger.error("user_id is missing in the request data.")
            return Response({"error": "user_id parameter is required."}, status=400)

        # user_id로 사용자 확인
        user = get_object_or_404(User, user_id=user_id)

        # product_id와 user로 Product 확인
        instance = get_object_or_404(Product, product_id=product_id, user=user)

        logger.info(f"Product found: {instance} for user_id: {user_id}")

        # 요청 데이터로 유효성 검사
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            logger.info("Validation succeeded.")
            self.perform_update(serializer)
            return Response(serializer.data, status=200)

        logger.error(f"Validation failed with errors: {serializer.errors}")
        return Response(serializer.errors, status=400)
