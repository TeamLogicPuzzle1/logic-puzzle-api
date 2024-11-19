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
    permission_classes = [permissions.IsAuthenticated]
    queryset = FoodWaste.objects.all()
    serializer_class = FoodWasteSerializer

    @swagger_auto_schema(
        request_body=FoodWasteSerializer,
        responses={201: FoodWasteSerializer},
        operation_description="Create a food waste record using user_id."
    )
    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"message": "유저를 찾을 수 없습니다.", "data": False}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, user_id=user_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user=user)
            logger.info(
                f"Created food waste record: User ID={user_id}, Quantity={instance.quantity}, Date Recorded={instance.date_recorded}")
            return Response({"message": "저장이 완료되었습니다.", "data": True}, status=status.HTTP_201_CREATED)

        return Response({"message": "저장에 실패하였습니다.", "data": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        manual_parameters=[user_id_param],
        responses={200: FoodWasteSerializer(many=True)},
        operation_description="List all food waste records for a specific user."
    )
    def list(self, request, *args, **kwargs):
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
        responses={200: 'Daily statistics of food waste'},
        operation_description="Get daily statistics of food waste for a specific user."
    )
    @action(detail=False, methods=['get'], url_path='stats/daily')
    def get_daily_stats(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id parameter is required."}, status=400)

        user = get_object_or_404(User, user_id=user_id)
        start_date = FoodWaste.objects.filter(user=user).earliest('date').date
        daily_data = get_daily_statistics(user=user, start_date=start_date)
        return Response({'daily_statistics': daily_data})

    @swagger_auto_schema(
        manual_parameters=[user_id_param],
        responses={200: 'Weekly statistics of food waste'},
        operation_description="Get weekly statistics of food waste for a specific user."
    )
    @action(detail=False, methods=['get'], url_path='stats/weekly')
    def get_weekly_stats(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id parameter is required."}, status=400)

        user = get_object_or_404(User, user_id=user_id)
        start_date = FoodWaste.objects.filter(user=user).earliest('date').date
        weekly_data = get_weekly_statistics(user=user, start_date=start_date)
        return Response({'weekly_statistics': weekly_data})

    @swagger_auto_schema(
        manual_parameters=[user_id_param],
        responses={200: 'Monthly statistics of food waste'},
        operation_description="Get monthly statistics of food waste for a specific user."
    )
    @action(detail=False, methods=['get'], url_path='stats/monthly')
    def get_monthly_stats(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id parameter is required."}, status=400)

        user = get_object_or_404(User, user_id=user_id)
        start_date = FoodWaste.objects.filter(user=user).earliest('date').date
        monthly_data = get_monthly_statistics(user=user, start_date=start_date)
        return Response({'monthly_statistics': monthly_data})

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

        if not user_id or quantity is None:
            return Response({"error": "user_id and quantity parameters are required."}, status=400)

        if quantity <= 0:
            return Response({"error": "The quantity to reduce must be greater than zero."}, status=400)

        user = get_object_or_404(User, user_id=user_id)
        success = reduce_food_waste(user, quantity)

        if not success:
            return Response({"error": "No food waste available to reduce."}, status=400)

        return Response({"message": f"Reduced {quantity}L from the latest record."}, status=200)

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

        return Response({"message": f"Deleted all food waste records for user_id: {user_id}."}, status=200)
