from django.db import models

import user.models
import uuid
from datetime import date


class Product(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255)  # 상품 이름 (필수)
    expiration_date = models.DateField(default=date.today, null=False, blank=False)  # 유통 기한 (필수)
    category = models.IntegerField(
        choices=[
            (1, '미분류'),
            (2, '고기'),
            (3, '해산물'),
            (4, '유제품'),
            (5, '야채'),
            (6, '음료'),
            (7, '과일'),
            (8, '기타')
        ],
        default=1  # 기본값
    )  # 카테고리 (필수)
    location = models.IntegerField(
        choices=[
            (1, '냉장'),
            (2, '냉동'),
            (3, '상온'),
            (4, '미분류')
        ],
        default=1  # 기본값
    )  # 장소 선택 (필수)
    quantity = models.IntegerField(default=1)  # 수량 (필수, 기본값 1)
    memo = models.TextField(blank=True, null=True)  # 메모 (선택)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # 이미지 파일 (선택)
    user = models.ForeignKey(user.models.User, on_delete=models.PROTECT)  # 사용자 (필수)

    def __str__(self):
        return f"{self.name} - {self.expiration_date}"

    class Meta:
        db_table = 'production'
