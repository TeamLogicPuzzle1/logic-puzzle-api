from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)  # 상품 이름

    expiration_date = models.DateField(null=True, blank=True)  # 유통 기한
    category = models.CharField(max_length=255, blank=True, null=True)  # 카테고리
    location = models.CharField(
        max_length=255,
        choices=[
            ('냉장', '냉장'),
            ('냉동', '냉동'),
            ('실외', '실외')
        ],
        blank=True,  # 선택 사항으로 유지
        null=True
    )  # 장소 선택
    quantity = models.IntegerField(blank=True, null=True)  # 수량
    memo = models.TextField(blank=True, null=True)  # 메모
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # 이미지 파일 필드 추가

    def __str__(self):
        return f"{self.name} - {self.expiration_date}"

    class Meta:
        db_table = 'product'  # 데이터베이스 테이블 이름
