from django.db import models

class FoodWaste(models.Model):
    quantity = models.FloatField()  # 음식물 쓰레기 양 (리터 단위)
    date = models.DateField()  # 날짜

    def __str__(self):
        return f"{self.quantity} L on {self.date}"