from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=30)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'