from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)  # 상품 이름
    expiration_date = models.DateField()  # 유통기한
    ocr = models.CharField(max_length=255, blank=True, null=True)  # OCR 데이터
    barcode = models.CharField(max_length=255, blank=True, null=True)  # 바코드 데이터
    category = models.CharField(max_length=255, blank=True, null=True)  # 카테고리
    location = models.CharField(max_length=255, choices=[
        ('냉장', '냉장'),
        ('냉동', '냉동'),
        ('실외', '실외')
    ], blank=True, null=True)  # 장소 선택
    quantity = models.IntegerField(blank=True, null=True)  # 수량
    memo = models.TextField(blank=True, null=True)  # 메모

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'production'
