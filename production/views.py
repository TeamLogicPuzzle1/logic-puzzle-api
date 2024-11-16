from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ProductCreateSerializer
from .models import Product
from user.models import User
from .servicelayer import extract_and_parse_expiration_date
from rest_framework import viewsets, status, permissions
import logging
from rest_framework.decorators import action

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    lookup_field = 'product_id'

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        return get_object_or_404(queryset, **filter_kwargs)

    @swagger_auto_schema(
        request_body=ProductCreateSerializer,
        responses={201: ProductCreateSerializer},
        operation_description="Create a product with an optional image file using user_id parameter. If an image is provided, it attempts to extract the expiration date."
    )
    def create_with_image(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id parameter is required."}, status=400)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()

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

            response_serializer = self.get_serializer(product)
            return Response(response_serializer.data, status=201)

        return Response(serializer.errors, status=400)

    user_id_param = openapi.Parameter(
        'user_id', openapi.IN_QUERY, description="Filter products by user ID", type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(
        manual_parameters=[user_id_param],
        operation_description="List all products for the authenticated user or filter by user_id.",
        responses={200: ProductCreateSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        if user_id:
            user = get_object_or_404(User, user_id=user_id)
            queryset = Product.objects.filter(user=user)
        else:
            queryset = Product.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductCreateSerializer,
        responses={200: ProductCreateSerializer},
        operation_description="Update a product by product_id with provided data."
    )
    def update(self, request, product_id=None):
        product = self.get_object()

        # 요청 데이터 복사
        data = request.data.copy()

        # user_id 처리 및 검증
        user_id = data.get("user_id")
        if user_id:
            user = get_object_or_404(User, user_id=user_id)
            data['user'] = user.pk  # User 객체의 ID를 직접 설정

        # Serializer로 업데이트 처리
        serializer = self.get_serializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'name', openapi.IN_QUERY, description="Search product by name", type=openapi.TYPE_STRING
            )
        ],
        operation_description="Search for products by their name.",
        responses={200: ProductCreateSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='search-by-name')
    def search_by_name(self, request):
        product_name = request.query_params.get('name', None)

        if not product_name:
            return Response({"error": "Product name parameter 'name' is required."}, status=status.HTTP_400_BAD_REQUEST)

        # 이름에 해당하는 상품 필터링
        queryset = self.get_queryset().filter(name__icontains=product_name)

        if not queryset.exists():
            return Response({"message": "No products found with the given name."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
