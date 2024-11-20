import logging
from food_waste.models import FoodWaste
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
from calendar import monthrange
# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def convert_quantity_to_liter(quantity_index):
    """Convert quantity index to actual liter value."""
    quantity_mapping = dict(FoodWaste.QUANTITY_CHOICES)  # {0: '1L', 1: '2L', ...}
    liter_value = quantity_mapping.get(quantity_index)
    if liter_value:
        return int(liter_value.rstrip('L'))  # '10L' -> 10
    return 0

def get_daily_statistics(user, start_date):
    """
    일별 데이터를 반환
    """
    today = timezone.now().date()
    days_difference = (today - start_date).days

    daily_data = [
        {
            "date": (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
            "total_waste": sum(
                convert_quantity_to_liter(record.quantity)
                for record in FoodWaste.objects.filter(
                    user=user,
                    date=(start_date + timedelta(days=i))
                )
            )
        }
        for i in range(days_difference + 1)
    ]
    return daily_data

def get_weekly_statistics(user, start_date):
    """
    주별 데이터를 반환 (최대 4주)
    """
    food_waste_records = FoodWaste.objects.filter(user=user, date__gte=start_date).order_by('date')
    if not food_waste_records.exists():
        return []

    weekly_data = []
    current_week = []
    week_start_date = food_waste_records.first().date
    week_end_date = week_start_date + timedelta(days=6)

    for record in food_waste_records:
        if record.date > week_end_date:
            weekly_data.append({
                "week_start": week_start_date.strftime('%Y-%m-%d'),
                "week_end": week_end_date.strftime('%Y-%m-%d'),
                "daily_data": current_week,
                "total_waste": sum(day["total_waste"] for day in current_week),
            })
            week_start_date = record.date
            week_end_date = week_start_date + timedelta(days=6)
            current_week = []

        current_week.append({
            "date": record.date.strftime('%Y-%m-%d'),
            "total_waste": convert_quantity_to_liter(record.quantity),  # 변환 추가
        })

    if current_week:
        weekly_data.append({
            "week_start": week_start_date.strftime('%Y-%m-%d'),
            "week_end": week_end_date.strftime('%Y-%m-%d'),
            "daily_data": current_week,
            "total_waste": sum(day["total_waste"] for day in current_week),
        })

    return weekly_data[-4:]


def get_monthly_statistics(user, start_date):
    """
    월별 데이터를 반환 (달력 기준, 최대 12달)
    """
    food_waste_records = FoodWaste.objects.filter(user=user, date__gte=start_date).order_by('date')
    if not food_waste_records.exists():
        return []

    monthly_data = []
    current_date = start_date

    while current_date <= timezone.now().date():
        _, last_day = monthrange(current_date.year, current_date.month)
        month_start = current_date.replace(day=1)
        month_end = current_date.replace(day=last_day)

        month_records = food_waste_records.filter(date__range=[month_start, month_end])
        daily_data = [
            {
                "date": record.date.strftime('%Y-%m-%d'),
                "total_waste": convert_quantity_to_liter(record.quantity)  # 변환 추가
            }
            for record in month_records
        ]

        monthly_data.append({
            "month_start": month_start.strftime('%Y-%m-%d'),
            "month_end": month_end.strftime('%Y-%m-%d'),
            "daily_data": daily_data,
            "total_waste": sum(day["total_waste"] for day in daily_data),  # 합산 수정
        })

        current_date = (month_end + timedelta(days=1))

    return monthly_data[-12:]



def reduce_food_waste(user, quantity):
    """
    음식물 쓰레기 양을 줄이는 함수 (기존 로직 유지)
    """
    today = timezone.now().date()
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
