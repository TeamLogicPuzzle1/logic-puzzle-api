from django.db import models

import user.models


# Create your models here.
class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user.models.User, max_length=20, on_delete=models.PROTECT)
    profile_name = models.CharField(max_length=20)
    pin_num = models.CharField(max_length=128, null=False, blank=False)
    leader_yn = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profile'