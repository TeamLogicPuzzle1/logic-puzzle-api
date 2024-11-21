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
from django.utils import timezone
from django.db import transaction

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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='User ID'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity index (0 to 5)'),
                'action_type': openapi.Schema(type=openapi.TYPE_INTEGER, description="Action type: 0 for add, 1 for reduce"),
            },
            required=['user_id', 'quantity', 'action_type']
        ),
        responses={200: 'Successfully processed food waste record.'},
        operation_description="Add or reduce food waste record based on action_type."
    )
    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        quantity_index = request.data.get("quantity")
        action_type = request.data.get("action_type")

        # 입력값 검증
        if not user_id or quantity_index is None or action_type is None:
            logger.error("Missing required parameters: user_id, quantity, action_type.")
            return Response({"error": "user_id, quantity, and action_type parameters are required."}, status=400)

        if action_type not in [0, 1]:
            logger.error(f"Invalid action_type: {action_type}")
            return Response({"error": "Invalid action_type. Use 0 for addition, 1 for reduction."}, status=400)

        if quantity_index < 0 or quantity_index >= len(FoodWaste.QUANTITY_CHOICES):
            logger.error(f"Invalid quantity index: {quantity_index}")
            return Response({"error": "Invalid quantity index."}, status=400)

        # 사용자 객체 가져오기
        user = get_object_or_404(User, user_id=user_id)

        # QUANTITY_CHOICES 매핑
        quantity_mapping = dict(FoodWaste.QUANTITY_CHOICES)
        quantity_liter = quantity_mapping.get(quantity_index)

        if quantity_liter is None:
            logger.error(f"Invalid quantity index mapping: {quantity_index}")
            return Response({"error": "Invalid quantity index mapping."}, status=400)

        quantity_value = int(quantity_liter.rstrip('L'))  # quantity index -> literal value

        try:
            if action_type == 0:  # 추가 로직
                FoodWaste.objects.create(
                    user=user,
                    quantity=quantity_index,
                    action_type=0,
                    date_recorded=timezone.now().date()
                )
                logger.info(f"Added {quantity_value}L for user_id {user_id}.")
                return Response({"message": f"Added {quantity_value}L to food waste records."}, status=201)

            elif action_type == 1:  # 감소 로직
                today = timezone.now().date()
                queryset = FoodWaste.objects.filter(user=user, date_recorded=today).order_by('-date_recorded')

                if not queryset.exists():
                    logger.error(f"No food waste available to reduce for user_id: {user.user_id}.")
                    return Response({"error": "No food waste available to reduce."}, status=400)

                total_available_liter = sum(int(quantity_mapping[record.quantity].rstrip('L')) for record in queryset)
                if total_available_liter < quantity_value:
                    logger.error(f"Cannot reduce {quantity_value}L. Available quantity is {total_available_liter}L.")
                    return Response({"error": f"Cannot reduce {quantity_value}L. Available quantity is {total_available_liter}L."}, status=400)

                # 감소 처리
                remaining_liter = quantity_value
                with transaction.atomic():
                    for record in queryset:
                        if remaining_liter <= 0:
                            break

                        record_liter = int(quantity_mapping[record.quantity].rstrip('L'))

                        if record_liter <= remaining_liter:
                            logger.info(f"Reducing entire {record_liter}L from record ID {record.id}")
                            remaining_liter -= record_liter
                            record.delete()
                        else:
                            new_quantity_liter = record_liter - remaining_liter
                            try:
                                record.quantity = next(
                                    key for key, value in quantity_mapping.items() if value == f"{new_quantity_liter}L"
                                )
                                record.save()
                                logger.info(f"Reduced quantity to {new_quantity_liter}L for record ID {record.id}")
                            except StopIteration:
                                logger.error(f"Failed to map new quantity: {new_quantity_liter}L")
                                return Response({"error": "Failed to reduce due to an internal mapping error."}, status=500)

                            remaining_liter = 0

                logger.info(f"Successfully reduced {quantity_value}L for user_id {user.user_id}.")
                return Response({"message": f"Reduced {quantity_value}L from the records."}, status=200)

        except Exception as e:
            logger.error(f"Error while processing food waste for user_id {user_id}: {e}")
            return Response({"error": "Failed to process food waste record."}, status=500)

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