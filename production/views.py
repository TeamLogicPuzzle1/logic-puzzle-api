from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializers import ProductCreateSerializer
from .models import Product
from user.models import User
from .servicelayer import extract_and_parse_expiration_date
from rest_framework import viewsets
import logging
from rest_framework import permissions

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    lookup_field = 'product_id'  # 기본 조회 필드를 product_id로 설정

    @swagger_auto_schema(
        request_body=ProductCreateSerializer,
        responses={201: ProductCreateSerializer},
        operation_description="Create a product with an optional image file using user_id parameter. If an image is provided, it attempts to extract the expiration date."
    )
    @action(detail=False, methods=['post'], url_path='create-with-image')
    def create_with_image(self, request):
        # user_id 파라미터로 유저 조회
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id parameter is required."}, status=400)

        # 상품 생성 처리
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()  # 이미 serializer에서 user를 처리하므로 별도로 user 추가 전달하지 않음

            # 이미지 파일 처리
            image = request.FILES.get('image')
            if image:
                logger.info(f"Received image file: {image.name}, size: {image.size}")

                try:
                    # OCR 기능을 사용해 유통기한 추출
                    expiration_date = extract_and_parse_expiration_date(image)
                    if expiration_date:
                        product.expiration_date = expiration_date
                        product.save(update_fields=['expiration_date'])  # 유통기한 정보만 업데이트
                    else:
                        logger.warning("No expiration date could be extracted from the image.")

                except Exception as e:
                    logger.exception(f"Error processing image: {str(e)}")
                    return Response({"error": str(e)}, status=400)

            # 업데이트된 product 객체로 새로운 serializer 생성 후 응답
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
        # 특정 사용자의 모든 제품 조회
        user_id = request.query_params.get('user_id')
        if user_id:
            user = get_object_or_404(User, user_id=user_id)
            queryset = Product.objects.filter(user=user)
        else:
            queryset = Product.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
