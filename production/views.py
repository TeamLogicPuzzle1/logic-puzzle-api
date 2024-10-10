from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ProductCreateSerializer
from .models import Product
from .servicelayer import extract_expiration_date_from_image
from rest_framework import viewsets
import os
from dotenv import load_dotenv
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .env 파일에서 환경 변수 로드
load_dotenv()

# Google Cloud Vision API 인증 설정 함수
def setup_google_vision():
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path or not os.path.exists(credentials_path):
        raise FileNotFoundError("Google Cloud credentials file not found. Check the path in your .env file.")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# Google Vision API 인증 설정
setup_google_vision()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    parser_classes = (MultiPartParser, FormParser)  # 파일 업로드를 처리하기 위한 파서 설정

    @swagger_auto_schema(
        request_body=ProductCreateSerializer,
        responses={201: ProductCreateSerializer},
        operation_description="Create a product with an optional image file."
    )
    @action(detail=False, methods=['post'], url_path='create-with-image')
    def create_with_image(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()

            # 이미지 파일 처리
            image = request.FILES.get('image')
            if not image:
                return Response({"error": "Image file is required."}, status=400)  # 이미지가 없는 경우 에러 메시지 추가

            logger.info(f"Received image file: {image.name}, size: {image.size}")

            try:
                expiration_date = extract_expiration_date_from_image(image)
                if expiration_date:
                    product.expiration_date = expiration_date
                    product.save()
                else:
                    logger.warning("No expiration date could be extracted.")
                    return Response({"error": "No expiration date could be extracted."}, status=400)

            except Exception as e:  # 예외 처리 추가
                logger.exception(f"Error processing image: {str(e)}")
                return Response({"error": str(e)}, status=400)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)