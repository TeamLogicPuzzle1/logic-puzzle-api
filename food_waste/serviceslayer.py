# serviceslayer.py
from food_waste.models import FoodWaste
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

def get_daily_statistics():
    today = timezone.now().date()
    daily_data = FoodWaste.objects.filter(date_recorded=today).aggregate(total_quantity=Sum('quantity'))
    return daily_data

def get_weekly_statistics():
    now = timezone.now()
    start_of_week = now - timedelta(days=now.weekday())
    weekly_data = FoodWaste.objects.filter(date_recorded__gte=start_of_week).aggregate(total_quantity=Sum('quantity'))
    return weekly_data

def get_monthly_statistics():
    now = timezone.now()
    start_of_month = now.replace(day=1)
    monthly_data = FoodWaste.objects.filter(date_recorded__gte=start_of_month).aggregate(total_quantity=Sum('quantity'))
    return monthly_data