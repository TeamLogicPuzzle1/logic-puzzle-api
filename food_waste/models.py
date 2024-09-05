from django.db import models
from django.core.exceptions import ValidationError

class FoodWaste(models.Model):
    quantity = models.FloatField()  # 음식물 쓰레기 양 (리터 단위)
    date_recorded = models.DateField(db_index=True)  # 날짜 (인덱스 추가)

    def __str__(self):
        return f"{self.quantity} L on {self.date_recorded}"

    def clean(self):
        # 유효성 검사: 양이 음수일 수 없음
        if self.quantity < 0:
            raise ValidationError('Quantity cannot be negative.')

    class Meta:
        ordering = ['-date_recorded']  # 기본 정렬 기준 설정