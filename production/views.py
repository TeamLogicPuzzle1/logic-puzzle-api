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
from .serializers import ProductCreateSerializer, ExpirationDateExtractSerializer
from .servicelayer import extract_and_parse_expiration_date
from datetime import date, timedelta

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
            return Product.objects.none()

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
        manual_parameters=[
            user_id_param, name_param, category_param, location_param,
            openapi.Parameter(
                'filter_type', openapi.IN_QUERY,
                description="1: Imminent products (7 days or less), 2: Expired products",
                type=openapi.TYPE_STRING
            )
        ],
        operation_description="List all products filtered by optional parameters, with summary in 'data' and items in 'List'.",
        responses={200: "Custom response with data and List"}
    )
    def list(self, request, *args, **kwargs):
        """
        Return filtered product list with summary data (imminent, expired counts).
        """
        filter_type = request.query_params.get('filter_type')
        queryset = self.get_queryset()

        # Current date
        today = date.today()
        upcoming_date = today + timedelta(days=7)

        # Apply filter conditions
        if filter_type == "1":  # Imminent products
            queryset = queryset.filter(expiration_date__gte=today, expiration_date__lte=upcoming_date)
        elif filter_type == "2":  # Expired products
            queryset = queryset.filter(expiration_date__lt=today)

        # Classify products (imminent, expired counts)
        imminent_count = queryset.filter(expiration_date__gte=today, expiration_date__lte=upcoming_date).count()
        expired_count = queryset.filter(expiration_date__lt=today).count()

        # Serialize products
        serializer = self.get_serializer(queryset, many=True)

        # Structured response
        response_data = {
            "data": {
                "imminent": imminent_count,  # Changed key to 'imminent'
                "expired": expired_count  # Changed key to 'expired'
            },
            "List": serializer.data  # Serialized product list
        }

        return Response(response_data, status=200)
    @swagger_auto_schema(
        operation_description="Extract expiration date from an uploaded image file.",
        request_body=ExpirationDateExtractSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'expiration_date': openapi.Schema(type=openapi.TYPE_STRING, format='date',
                                                      description='Extracted expiration date'),
                }
            ),
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    @action(detail=False, methods=['post'], url_path='extract-expiration-date', url_name='extract_expiration_date')
    def extract_expiration_date(self, request):
        """
        이미지에서 소비기한 추출
        """
        serializer = ExpirationDateExtractSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            try:
                expiration_date = extract_and_parse_expiration_date(image)
                if expiration_date:
                    return Response({"expiration_date": expiration_date}, status=200)
                else:
                    return Response({"error": "No expiration date could be extracted from the image."}, status=400)
            except Exception as e:
                logger.exception(f"Error extracting expiration date: {str(e)}")
                return Response({"error": str(e)}, status=500)
        return Response(serializer.errors, status=400)

    def create(self, request, *args, **kwargs):
        """
        상품 생성 API (이미지 없이 소비기한 직접 입력)
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 상품 저장
            product = serializer.save()
            return Response(serializer.data, status=201)

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

        user_id = request.data.get('user_id')
        if not user_id:
            logger.error("user_id is missing in the request data.")
            return Response({"error": "user_id parameter is required."}, status=400)

        user = get_object_or_404(User, user_id=user_id)

        instance = get_object_or_404(Product, product_id=product_id, user=user)

        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=200)

        logger.error(f"Validation failed with errors: {serializer.errors}")
        return Response(serializer.errors, status=400)
