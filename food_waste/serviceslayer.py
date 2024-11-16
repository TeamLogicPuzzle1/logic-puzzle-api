import logging
from food_waste.models import FoodWaste
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_daily_statistics(user):
    today = timezone.now().date()
    daily_data = FoodWaste.objects.filter(user=user, date_recorded=today).aggregate(total_quantity=Sum('quantity'))
    return daily_data


def get_weekly_statistics(user):
    now = timezone.now()
    start_of_week = now - timedelta(days=now.weekday())
    weekly_data = FoodWaste.objects.filter(user=user, date_recorded__gte=start_of_week).aggregate(
        total_quantity=Sum('quantity'))
    return weekly_data


def get_monthly_statistics(user):
    now = timezone.now()
    start_of_month = now.replace(day=1)
    monthly_data = FoodWaste.objects.filter(user=user, date_recorded__gte=start_of_month).aggregate(
        total_quantity=Sum('quantity'))
    return monthly_data


def reduce_food_waste(user, quantity):
    today = timezone.now().date()
    # 오늘 날짜의 레코드를 가져오되, quantity가 0보다 큰 레코드 중 가장 최신 것을 가져옴
    queryset = FoodWaste.objects.filter(user=user, date_recorded=today, quantity__gt=0).order_by('-date_recorded')
    logger.info(f"Queryset size for user {user.user_id} on {today}: {queryset.count()}")

    if not queryset.exists():
        logger.error(f"No food waste available to reduce for user_id: {user.user_id}.")
        return False

    latest_record = queryset.first()
    logger.info(f"Latest record found: User ID={user.user_id}, Quantity={latest_record.quantity}, Date Recorded={latest_record.date_recorded}")

    if latest_record.quantity < quantity:
        logger.error(f"The quantity to reduce ({quantity}) is greater than the recorded quantity ({latest_record.quantity}).")
        return False

    # 양 감소
    latest_record.quantity -= quantity
    latest_record.save()

    logger.info(f"Successfully reduced {quantity}L from the latest record for user_id: {user.user_id}. New quantity: {latest_record.quantity}")

    return True
