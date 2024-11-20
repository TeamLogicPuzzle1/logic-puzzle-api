from django.db import models


# Create your models here.
class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=100)
    material_name = models.TextField()

    class Meta:
        db_table = 'recipe'