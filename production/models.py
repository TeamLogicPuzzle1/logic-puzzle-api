import uuid
from datetime import date

from django.db import models

import user.models


class Product(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255)  # 상품 이름 (필수)
    expiration_date = models.DateField(default=date.today, null=False, blank=False)  # 유통 기한 (필수)
    category = models.IntegerField(
        choices=[
            (0, '미분류'),
            (1, '고기'),
            (2, '해산물'),
            (3, '유제품'),
            (4, '야채'),
            (5, '음료'),
            (6, '과일'),
            (7, '기타')
        ],
        default=0  # 기본값
    )  # 카테고리 (필수)
    location = models.IntegerField(
        choices=[
            (0, '냉장'),
            (1, '냉동'),
            (2, '상온'),
            (3, '미분류')
        ],
        default=0  # 기본값
    )  # 장소 선택 (필수)
    quantity = models.IntegerField(default=1)  # 수량 (필수, 기본값 1)
    memo = models.TextField(blank=True, null=True)  # 메모 (선택)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # 이미지 파일 (선택)
    user = models.ForeignKey(user.models.User, on_delete=models.PROTECT)  # 사용자 (필수)

    def __str__(self):
        return f"{self.name} - {self.expiration_date}"

    class Meta:
        db_table = 'production'
