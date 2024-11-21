# Generated by Django 5.0.7 on 2024-11-17 02:02

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.IntegerField(choices=[(1, '미분류'), (2, '고기'), (3, '해산물'), (4, '유제품'), (5, '야채'), (6, '음료'), (7, '과일'), (8, '기타')], default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='expiration_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='product',
            name='location',
            field=models.IntegerField(choices=[(1, '냉장'), (2, '냉동'), (3, '상온'), (4, '미분류')], default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
