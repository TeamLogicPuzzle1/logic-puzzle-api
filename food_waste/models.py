# models.py
from django.db import models

class FoodWaste(models.Model):
    QUANTITY_CHOICES = [
        (1, '1L'),
        (3, '3L'),
        (5, '5L'),
        (10, '10L'),
        (20, '20L'),  # 20L 추가
    ]

    quantity = models.IntegerField(choices=QUANTITY_CHOICES)  # 필수 필드
    date_recorded = models.DateField(auto_now_add=True)  # 객체 생성 시 현재 날짜 자동 설정

    def __str__(self):
        return f"{self.get_quantity_display()} - {self.date_recorded}"

    class Meta:
        db_table = 'food_waste'