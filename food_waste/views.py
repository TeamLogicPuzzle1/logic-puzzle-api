# views.py
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Sum
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import FoodWaste
from .serializers import FoodWasteSerializer
from .serviceslayer import get_daily_statistics, get_weekly_statistics, get_monthly_statistics

class FoodWasteViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FoodWaste.objects.all()
    serializer_class = FoodWasteSerializer
    parser_classes = [MultiPartParser, FormParser]  # 파일 업로드를 위한 파서 설정


    @swagger_auto_schema(
        request_body=FoodWasteSerializer,
        responses={201: FoodWasteSerializer},
        operation_description="Create a food waste record."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_stats(self, start_date, end_date):
        stats = self.queryset.filter(date_recorded__gte=start_date, date__lte=end_date).aggregate(total=Sum('amount'))
        return stats['total'] or 0


    @swagger_auto_schema(
        responses={200: 'Total quantity of food waste for today'},
        operation_description="Get daily statistics of food waste."
    )
    @action(detail=False, methods=['get'], url_path='stats/daily')
    def get_daily_stats(self, request):
        daily_data = get_daily_statistics()
        return Response({'total_quantity': daily_data.get('total_quantity', 0)})

    @swagger_auto_schema(
        responses={200: 'Total quantity of food waste for the week'},
        operation_description="Get weekly statistics of food waste."
    )
    @action(detail=False, methods=['get'], url_path='stats/weekly')
    def get_weekly_stats(self, request):
        weekly_data = get_weekly_statistics()
        return Response({'total_quantity': weekly_data.get('total_quantity', 0)})

    @swagger_auto_schema(
        responses={200: 'Total quantity of food waste for the month'},
        operation_description="Get monthly statistics of food waste."
    )
    @action(detail=False, methods=['get'], url_path='stats/monthly')
    def get_monthly_stats(self, request):
        monthly_data = get_monthly_statistics()
        return Response({'total_quantity': monthly_data.get('total_quantity', 0)})