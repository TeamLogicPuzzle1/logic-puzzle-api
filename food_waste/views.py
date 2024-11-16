from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
import logging

from .models import FoodWaste
from .serializers import FoodWasteSerializer
from user.models import User
from .serviceslayer import get_daily_statistics, get_weekly_statistics, get_monthly_statistics, reduce_food_waste

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_id_param = openapi.Parameter(
    'user_id', openapi.IN_QUERY, description="User ID to filter food waste records", type=openapi.TYPE_STRING
)


class FoodWasteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]  # JWT 인증 제거, 모든 접근 허용
    queryset = FoodWaste.objects.all()
    serializer_class = FoodWasteSerializer

    @swagger_auto_schema(
        request_body=FoodWasteSerializer,
        responses={201: FoodWasteSerializer},
        operation_description="Create a food waste record using user_id."
    )
    def create(self, request, *args, **kwargs):
        # user_id 파라미터로 유저 조회
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id parameter is required."}, status=400)

        user = get_object_or_404(User, user_id=user_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user=user)
            logger.info(
                f"Created food waste record: User ID={user_id}, Quantity={instance.quantity}, Date Recorded={instance.date_recorded}")
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        manual_parameters=[user_id_param],
        responses={200: FoodWasteSerializer(many=True)},
        operation_description="List all food waste records for a specific user."
    )
    def list(self, request, *args, **kwargs):
        # 특정 사용자의 모든 음식물 쓰레기 기록 조회
        user_id = request.query_params.get('user_id')
        if user_id:
            user = get_object_or_404(User, user_id=user_id)
            queryset = FoodWaste.objects.filter(user=user)
        else:
            return Response({"error": "user_id parameter is required for listing records."}, status=400)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[user_id_param],
        responses={200: 'Total quantity of food waste for today'},
        operation_description="Get daily statistics of food waste for a specific user."
    )
    @action(detail=False, methods=['get'], url_path='stats/daily')
    def get_daily_stats(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id parameter is required."}, status=400)

        user = get_object_or_404(User, user_id=user_id)
        daily_data = get_daily_statistics(user=user)
        return Response({'total_quantity': daily_data.get('total_quantity', 0)})

    @swagger_auto_schema(
        manual_parameters=[user_id_param],
        responses={200: 'Total quantity of food waste for the week'},
        operation_description="Get weekly statistics of food waste for a specific user."
    )
    @action(detail=False, methods=['get'], url_path='stats/weekly')
    def get_weekly_stats(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id parameter is required."}, status=400)

        user = get_object_or_404(User, user_id=user_id)
        weekly_data = get_weekly_statistics(user=user)
        return Response({'total_quantity': weekly_data.get('total_quantity', 0)})

    @swagger_auto_schema(
        manual_parameters=[user_id_param],
        responses={200: 'Total quantity of food waste for the month'},
        operation_description="Get monthly statistics of food waste for a specific user."
    )
    @action(detail=False, methods=['get'], url_path='stats/monthly')
    def get_monthly_stats(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id parameter is required."}, status=400)

        user = get_object_or_404(User, user_id=user_id)
        monthly_data = get_monthly_statistics(user=user)
        return Response({'total_quantity': monthly_data.get('total_quantity', 0)})

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='User ID'),
                'quantity': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount to reduce')
            },
            required=['user_id', 'quantity']
        ),
        responses={200: 'Reduced quantity of food waste'},
        operation_description="Reduce food waste quantity for the latest record of a user."
    )
    @action(detail=False, methods=['post'], url_path='reduce')
    def reduce(self, request):
        user_id = request.data.get("user_id")
        quantity = request.data.get("quantity")

        logger.info(f"Received reduce request with user_id: {user_id}, quantity: {quantity}")

        if not user_id or quantity is None:
            logger.error("Missing user_id or quantity in request.")
            return Response({"error": "user_id and quantity parameters are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if quantity <= 0:
            logger.error(f"Invalid quantity to reduce: {quantity}")
            return Response({"error": "The quantity to reduce must be greater than zero."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, user_id=user_id)
        success = reduce_food_waste(user, quantity)

        if not success:
            logger.error("No food waste available to reduce.")
            return Response({"error": "No food waste available to reduce."},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": f"Reduced {quantity}L from the latest record."
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[user_id_param],
        responses={200: 'All food waste records deleted for the user.'},
        operation_description="Delete all food waste records for a specific user."
    )
    @action(detail=False, methods=['delete'], url_path='delete-all')
    def delete_all(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id parameter is required."}, status=400)

        user = get_object_or_404(User, user_id=user_id)
        records_deleted, _ = FoodWaste.objects.filter(user=user).delete()

        logger.info(f"Deleted all food waste records for user_id: {user_id}. Total records deleted: {records_deleted}")

        return Response({
            "message": f"Deleted all food waste records for user_id: {user_id}."
        }, status=status.HTTP_200_OK)
