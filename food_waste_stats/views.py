from django.db.models import Sum
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from .models import FoodWaste
from .serializers import FoodWasteSerializer

class FoodWasteViewSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = FoodWaste.objects.all()
    serializer_class = FoodWasteSerializer

    @action(detail=False, methods=['get'])
    def daily_stats(self, request):
        today = timezone.now().date()
        stats = self.queryset.filter(date_recorded=today).aggregate(total=Sum('amount'))
        return Response({'date': today, 'total_amount': stats['total'] or 0})

    @action(detail=False, methods=['get'])
    def weekly_stats(self, request):
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        stats = self.queryset.filter(date_recorded__gte=start_of_week, date_recorded__lte=today).aggregate(total=Sum('amount'))
        return Response({'week_start': start_of_week, 'total_amount': stats['total'] or 0})

    @action(detail=False, methods=['get'])
    def monthly_stats(self, request):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        stats = self.queryset.filter(date_recorded__gte=start_of_month, date_recorded__lte=today).aggregate(total=Sum('amount'))
        return Response({'month_start': start_of_month, 'total_amount': stats['total'] or 0})