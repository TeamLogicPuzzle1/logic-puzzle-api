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
    quantity_mapping = dict(FoodWaste.QUANTITY_CHOICES)
    liter_value = quantity_mapping.get(quantity_index)
    if liter_value:
        return int(liter_value.rstrip('L'))  # '1L', '2L', ... -> 숫자 추출
    return 0  # quantity가 0일 경우 0을 반환


def get_daily_statistics(user, start_date):
    """
    일별 데이터를 반환, quantity=0 데이터를 명확히 처리하여 합산에 포함.
    """
    today = timezone.now().date()
    days_difference = (today - start_date).days

    # 날짜별 데이터를 생성
    daily_data = []
    for i in range(days_difference + 1):
        date = start_date + timedelta(days=i)

        # 해당 날짜의 모든 기록을 가져옵니다
        records = FoodWaste.objects.filter(user=user, date_recorded=date)

        # QUANTITY_CHOICES로 매핑하여 L 값을 합산
        quantity_mapping = dict(FoodWaste.QUANTITY_CHOICES)
        total_waste = sum(
            int(quantity_mapping[record.quantity].rstrip('L'))  # '1L' -> 1
            for record in records
        )

        # 로그로 디버깅 정보 추가
        logger.info(f"Date: {date}, Records: {list(records.values())}, Total Waste: {total_waste}L")

        daily_data.append({
            "date": date.strftime('%Y-%m-%d'),
            "total_waste": total_waste  # 합산 결과
        })

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



def reduce_food_waste(user, quantity_index):
    """음식물 쓰레기 기록에서 지정된 양을 줄이는 함수"""
    today = timezone.now().date()
    queryset = FoodWaste.objects.filter(user=user, date_recorded=today).order_by('-date_recorded')

    if not queryset.exists():
        logger.error(f"No food waste available to reduce for user_id: {user.user_id}.")
        return {"success": False, "message": "No food waste available to reduce."}

    # QUANTITY_CHOICES로 리터 값 매핑
    quantity_mapping = dict(FoodWaste.QUANTITY_CHOICES)
    reduce_liter = int(quantity_mapping[quantity_index].rstrip('L'))

    logger.info(f"Requested reduction: {reduce_liter}L")

    total_available_liter = sum(int(quantity_mapping[record.quantity].rstrip('L')) for record in queryset)
    logger.info(f"Total available: {total_available_liter}L")

    if total_available_liter < reduce_liter:
        logger.error(f"Cannot reduce {reduce_liter}L. Available quantity is {total_available_liter}L.")
        return {
            "success": False,
            "message": f"Cannot reduce {reduce_liter}L. Available quantity is {total_available_liter}L."
        }

    # 감소 처리
    remaining_liter = reduce_liter
    for record in queryset:
        if remaining_liter <= 0:
            break

        record_liter = int(quantity_mapping[record.quantity].rstrip('L'))

        if record_liter <= remaining_liter:
            logger.info(f"Reducing entire {record_liter}L from record ID {record.id}")
            remaining_liter -= record_liter
            record.quantity = 0  # 음식물 쓰레기 수량을 0으로 설정
        else:
            new_quantity_liter = record_liter - remaining_liter
            try:
                record.quantity = next(
                    key for key, value in quantity_mapping.items() if value == f"{new_quantity_liter}L"
                )
            except StopIteration:
                logger.error(f"Failed to map new quantity: {new_quantity_liter}L")
                return {
                    "success": False,
                    "message": f"Failed to reduce due to an internal mapping error."
                }
            remaining_liter = 0

        # 기록을 저장하여 변경 사항을 데이터베이스에 반영
        record.save()

        # 변경된 레코드를 최신 데이터로 갱신
        record.refresh_from_db()

    # 변경 후 상태를 로그로 출력
    updated_queryset = FoodWaste.objects.filter(user=user, date_recorded=today).order_by('-date_recorded')
    logger.info(f"Updated records after reduction: {[record.id for record in updated_queryset]}")

    if remaining_liter > 0:
        logger.warning(f"Unable to reduce full {reduce_liter}L, remaining {remaining_liter}L was not processed.")
    else:
        logger.info(f"Successfully reduced {reduce_liter}L for user_id {user.user_id}.")

    return {"success": True, "message": f"Reduced {reduce_liter}L from the records."}