from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ProductCreateSerializer
from .models import Product
from .servicelayer import extract_expiration_date_from_image
from rest_framework import viewsets
import os
from google.cloud import vision

# .env 파일에서 환경 변수 로드
load_dotenv()

# Google Cloud Vision API의 인증 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

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
            if image:
                expiration_date = extract_expiration_date_from_image(image)
                if expiration_date:
                    product.expiration_date = expiration_date
                    product.save()

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)