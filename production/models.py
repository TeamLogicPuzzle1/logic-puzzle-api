from django.db import models

from django.db import models

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    expiration_date = models.DateField()
    category = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, choices=[('refrigerated', '냉장'), ('frozen', '냉동'), ('outdoor', '실외')], blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
