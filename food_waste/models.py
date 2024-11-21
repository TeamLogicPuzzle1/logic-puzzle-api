import datetime

from django.core.exceptions import ValidationError
from django.db import models

import user.models


class FoodWaste(models.Model):
    QUANTITY_CHOICES = [
        (0, '1L'),
        (1, '2L'),  # 2L 추가
        (2, '3L'),
        (3, '5L'),
        (4, '10L'),
        (5, '20L')  # 20L 추가
    ]

    ACTION_TYPE_CHOICES = [
        (0, '+'),  # Addition
        (1, '-'),  # Reduction
    ]

    quantity = models.IntegerField(
        choices=QUANTITY_CHOICES,
        help_text="0 : 1L, 1 : 2L, 2 : 3L, 3 : 5L, 4 : 10L, 5 : 20L",
        default=0  # 음식물 쓰레기 양 (리터 단위, 필수 필드)
    )
    action_type = models.IntegerField(
        choices=ACTION_TYPE_CHOICES,
        help_text="Action type: 0 for addition (+), 1 for reduction (-)",
        default=0
    )
    date_recorded = models.DateField(auto_now_add=True)  # 객체 생성 시 현재 날짜 자동 설정
    date = models.DateField(db_index=True, default=datetime.date.today)  # 날짜 (인덱스 추가)
    user = models.ForeignKey(user.models.User, max_length=20, on_delete=models.PROTECT, default='', null=False)

    def __str__(self):
        action = dict(self.ACTION_TYPE_CHOICES).get(self.action_type)
        quantity = dict(self.QUANTITY_CHOICES).get(self.quantity)
        return f"{action} {quantity} on {self.date_recorded}"

    def clean(self):
        # 유효성 검사: 양이 음수일 수 없음
        if self.quantity < 0:
            raise ValidationError('Quantity cannot be negative.')

        # 유효성 검사: quantity 값이 QUANTITY_CHOICES에 포함되어 있는지 확인
        valid_choices = [choice[0] for choice in self.QUANTITY_CHOICES]  # 선택 가능한 값들 추출
        if self.quantity not in valid_choices:
            raise ValidationError(
                f'Quantity value {self.quantity} is not a valid choice. Valid choices are: {valid_choices}')

        # 유효성 검사: action_type 값이 ACTION_TYPE_CHOICES에 포함되어 있는지 확인
        valid_action_choices = [choice[0] for choice in self.ACTION_TYPE_CHOICES]
        if self.action_type not in valid_action_choices:
            raise ValidationError(
                f'Action type {self.action_type} is not valid. Valid choices are: {valid_action_choices}'
            )

    class Meta:
        ordering = ['-date']  # 기본 정렬 기준 설정
        db_table = 'food_waste'