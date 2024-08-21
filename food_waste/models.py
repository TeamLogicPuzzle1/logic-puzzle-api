from django.db import models

class FoodWaste(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=2)  # L 단위
    date = models.DateField()  # 날짜

    def __str__(self):
        return f'{self.amount}L on {self.date}'