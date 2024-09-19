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

    def get_stats(self, start_date, end_date):
        stats = self.queryset.filter(date_recorded__gte=start_date, date__lte=end_date).aggregate(total=Sum('amount'))
        return stats['total'] or 0

    @action(detail=False, methods=['get'])
    def daily_stats(self, request):
        today = timezone.now().date()
        total_amount = self.get_stats(today, today)
        return Response({'date': today, 'total_amount': total_amount})

    @action(detail=False, methods=['get'])
    def weekly_stats(self, request):
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        total_amount = self.get_stats(start_of_week, today)
        return Response({'week_start': start_of_week, 'total_amount': total_amount})

    @action(detail=False, methods=['get'])
    def monthly_stats(self, request):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        total_amount = self.get_stats(start_of_month, today)
        return Response({'month_start': start_of_month, 'total_amount': total_amount})