from django.core.exceptions import ValidationError
from django.db import models

import user.models


class FoodWaste(models.Model):
    QUANTITY_CHOICES = [
        (1, '1L'),
        (3, '3L'),
        (5, '5L'),
        (10, '10L'),
        (20, '20L'),  # 20L 추가
    ]

    quantity = models.FloatField(choices=QUANTITY_CHOICES)  # 음식물 쓰레기 양 (리터 단위, 필수 필드)
    date_recorded = models.DateField(auto_now_add=True)  # 객체 생성 시 현재 날짜 자동 설정
    date = models.DateField(db_index=True)  # 날짜 (인덱스 추가)
    user = models.ForeignKey(user.models.User, max_length=20, on_delete=models.PROTECT, default='', null=False)

    def __str__(self):
        return f"{self.quantity} L on {self.date_recorded}"

    def clean(self):
        # 유효성 검사: 양이 음수일 수 없음
        if self.quantity < 0:
            raise ValidationError('Quantity cannot be negative.')

    class Meta:
        ordering = ['-date']  # 기본 정렬 기준 설정
        db_table = 'food_waste'
