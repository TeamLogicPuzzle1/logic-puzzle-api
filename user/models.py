from django.contrib.auth.models import UserManager
from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'user_id'

    REQUIRED_FIELDS = []

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    is_anonymous = models.BooleanField(default=True)

    is_authenticated = models.BooleanField(default=True)

    def has_module_perm(self, app_label):
        return True

    objects = UserManager()

    class Meta:
        db_table = 'user'